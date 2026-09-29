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
