const toast = document.getElementById('toast');

function showToast(message) {
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  window.setTimeout(() => toast.classList.remove('show'), 2400);
}

document.querySelectorAll('[data-toast]').forEach((control) => {
  control.addEventListener('click', () => showToast(control.dataset.toast));
});

const menuTriggers = document.querySelectorAll('[data-menu-trigger]');

function closeMenus(exceptName) {
  document.querySelectorAll('[data-menu]').forEach((menu) => {
    if (menu.dataset.menu !== exceptName) {
      menu.classList.remove('open');
    }
  });

  menuTriggers.forEach((trigger) => {
    if (trigger.dataset.menuTrigger !== exceptName) {
      trigger.setAttribute('aria-expanded', 'false');
    }
  });
}

menuTriggers.forEach((trigger) => {
  trigger.addEventListener('click', (event) => {
    event.stopPropagation();
    const menuName = trigger.dataset.menuTrigger;
    const menu = document.querySelector(`[data-menu="${menuName}"]`);
    if (!menu) return;

    const shouldOpen = !menu.classList.contains('open');
    closeMenus(menuName);
    menu.classList.toggle('open', shouldOpen);
    trigger.setAttribute('aria-expanded', shouldOpen ? 'true' : 'false');
  });
});

document.addEventListener('click', () => closeMenus());
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMenus();
});

document.querySelectorAll('[data-demo-reset]').forEach((button) => {
  button.addEventListener('click', () => {
    closeMenus();
    window.location.href = '/demo/reset';
  });
});

const eventList = document.getElementById('event-list');
const filterButtons = document.querySelectorAll('[data-filter]');
const eventCards = document.querySelectorAll('[data-event-card]');
const resultCount = document.getElementById('result-count');
const emptyState = document.getElementById('empty-state');

function updateResultCount(count) {
  if (!resultCount) return;
  resultCount.textContent = `${count} ${count === 1 ? 'event' : 'events'} shown`;
}

function applyFilter(filterName) {
  if (!eventList || !eventCards.length) return;

  const currentMonth = eventList.dataset.currentMonth;
  let visibleCount = 0;

  eventCards.forEach((card) => {
    const inCurrentMonth = card.dataset.month === currentMonth;
    const isWeekend = card.dataset.weekend === 'true';
    const isVisible =
      filterName === 'all' ||
      (filterName === 'month' && inCurrentMonth) ||
      (filterName === 'weekend' && isWeekend);

    card.classList.toggle('hidden', !isVisible);
    if (isVisible) visibleCount += 1;
  });

  filterButtons.forEach((button) => {
    button.classList.toggle('active', button.dataset.filter === filterName);
  });

  updateResultCount(visibleCount);
  if (emptyState) emptyState.classList.toggle('hidden', visibleCount > 0);
}

filterButtons.forEach((button) => {
  button.addEventListener('click', () => applyFilter(button.dataset.filter));
});

applyFilter('all');

const eventTabButtons = document.querySelectorAll('[data-events-tab]');
const eventTabPanels = document.querySelectorAll('[data-events-panel]');

function showEventsTab(tabName) {
  eventTabButtons.forEach((button) => {
    button.classList.toggle('active', button.dataset.eventsTab === tabName);
  });

  eventTabPanels.forEach((panel) => {
    panel.classList.toggle('hidden', panel.dataset.eventsPanel !== tabName);
  });
}

eventTabButtons.forEach((button) => {
  button.addEventListener('click', () => showEventsTab(button.dataset.eventsTab));
});

const leaderboardTabButtons = document.querySelectorAll('[data-leaderboard-tab]');
const leaderboardPanels = document.querySelectorAll('[data-leaderboard-panel]');

function showLeaderboardTab(tabName) {
  leaderboardTabButtons.forEach((button) => {
    const isActive = button.dataset.leaderboardTab === tabName;
    button.classList.toggle('active', isActive);
    button.setAttribute('aria-pressed', isActive ? 'true' : 'false');
  });

  leaderboardPanels.forEach((panel) => {
    panel.classList.toggle('hidden', panel.dataset.leaderboardPanel !== tabName);
  });
}

leaderboardTabButtons.forEach((button) => {
  button.addEventListener('click', () => showLeaderboardTab(button.dataset.leaderboardTab));
});

document.querySelectorAll('[data-close-reassign]').forEach((button) => {
  button.addEventListener('click', () => {
    const panel = button.closest('details');
    if (panel) panel.open = false;
  });
});

const reportRangeButtons = document.querySelectorAll('[data-report-range]');

reportRangeButtons.forEach((button) => {
  button.addEventListener('click', () => {
    reportRangeButtons.forEach((rangeButton) => {
      const isActive = rangeButton === button;
      rangeButton.classList.toggle('active', isActive);
      rangeButton.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
    showToast(`Report range set to ${button.textContent.trim()}.`);
  });
});

const reportSearchInput = document.querySelector('[data-report-search]');
const reportDepartmentSelect = document.querySelector('[data-report-department]');
const reportRows = document.querySelectorAll('[data-report-row]');
const reportEmptyState = document.querySelector('[data-report-empty]');
const exportReportButton = document.querySelector('[data-export-report]');

function getVisibleReportRows() {
  return Array.from(reportRows).filter((row) => !row.classList.contains('hidden'));
}

function applyReportFilters() {
  if (!reportRows.length) return;

  const searchValue = reportSearchInput ? reportSearchInput.value.trim().toLowerCase() : '';
  const departmentValue = reportDepartmentSelect ? reportDepartmentSelect.value : 'all';
  let visibleCount = 0;

  reportRows.forEach((row) => {
    const matchesSearch = !searchValue || row.dataset.officer.includes(searchValue);
    const matchesDepartment =
      departmentValue === 'all' || row.dataset.department === departmentValue;
    const isVisible = matchesSearch && matchesDepartment;

    row.classList.toggle('hidden', !isVisible);
    if (isVisible) visibleCount += 1;
  });

  if (reportEmptyState) reportEmptyState.classList.toggle('hidden', visibleCount > 0);
}

if (reportSearchInput) reportSearchInput.addEventListener('input', applyReportFilters);
if (reportDepartmentSelect) reportDepartmentSelect.addEventListener('change', applyReportFilters);

function getReportCellText(row, index) {
  const cell = row.children[index];
  return cell ? cell.textContent.trim() : '';
}

function csvEscape(value) {
  return `"${String(value).replace(/"/g, '""')}"`;
}

if (exportReportButton) {
  exportReportButton.addEventListener('click', () => {
    const rows = getVisibleReportRows();
    const headers = ['Officer', 'Department', 'Events', 'Hours', 'Cancellations'];
    const csvRows = [
      headers.map(csvEscape).join(','),
      ...rows.map((row) =>
        [0, 1, 2, 3, 4].map((index) => csvEscape(getReportCellText(row, index))).join(',')
      ),
    ];

    const blob = new Blob([`${csvRows.join('\n')}\n`], { type: 'text/csv;charset=utf-8;' });
    const downloadUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = 'sode-volunteer-hours-demo.csv';
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(downloadUrl);
    showToast(`Exported ${rows.length} officer records.`);
  });
}
