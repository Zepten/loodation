<script>
  import { ArrowLeft, ArrowRight, Bell, ChevronDown, CircleHelp, Compass, Crown, Flame, Grid2X2, Home, Menu, Plus, Search, Settings2, ShieldCheck, Sparkles, Star, UserRound, Wallet, X } from 'lucide-svelte';

  const games = [
    { id: 'neon', title: 'Неоновые 7', category: 'Слоты', tag: 'ХИТ', players: '1,2k', win: 'x500', tone: 'neon', icon: '✦', subtitle: 'Поймай свою волну' },
    { id: 'moon', title: 'Лунная пыль', category: 'Слоты', tag: 'НОВИНКА', players: '846', win: 'x250', tone: 'moon', icon: '☾', subtitle: 'Выше облаков' },
    { id: 'dice', title: 'Кости судьбы', category: 'Казуальные', tag: '', players: '623', win: 'x100', tone: 'dice', icon: '⚄', subtitle: 'Твой ход — твой шанс' },
    { id: 'cards', title: 'Туз в рукаве', category: 'Карты', tag: '', players: '392', win: 'x50', tone: 'cards', icon: '♠', subtitle: 'Сыграем красиво?' },
    { id: 'cherry', title: 'Вишнёвый бум', category: 'Слоты', tag: '', players: '278', win: 'x300', tone: 'cherry', icon: '🍒', subtitle: 'Сладкая удача' },
    { id: 'orbit', title: 'Орбита', category: 'Казуальные', tag: '', players: '184', win: 'x80', tone: 'orbit', icon: '◉', subtitle: 'Поймай ритм' }
  ];
  const categories = ['Все игры', 'Слоты', 'Карты', 'Казуальные'];
  let page = 'home';
  let category = 'Все игры';
  let query = '';
  let selectedGame = null;
  let balance = 12480;
  let notice = '';
  let rolling = false;
  let result = '';
  let mobileMenu = false;

  $: filteredGames = games.filter((game) => (category === 'Все игры' || game.category === category) && game.title.toLowerCase().includes(query.toLowerCase()));
  const money = (value) => new Intl.NumberFormat('ru-RU').format(value);

  function openGame(game) {
    selectedGame = game;
    page = 'game';
    result = '';
    mobileMenu = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  function go(next) {
    page = next;
    selectedGame = null;
    mobileMenu = false;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  function showNotice(message) {
    notice = message;
    setTimeout(() => notice = '', 2600);
  }
  function playDemo() {
    if (rolling) return;
    const bet = 100;
    if (balance < bet) return showNotice('Недостаточно очков для демо-раунда');
    balance -= bet;
    rolling = true;
    result = '';
    setTimeout(() => {
      const won = Math.random() > 0.56;
      if (won) balance += 250;
      result = won ? 'Красиво! +250 очков' : 'В этот раз без выигрыша. Попробуешь ещё?';
      rolling = false;
    }, 900);
  }

  const nav = [
    { label: 'Главная', icon: Home, page: 'home' },
    { label: 'Все игры', icon: Grid2X2, page: 'catalog' },
    { label: 'Мои игры', icon: Star, page: 'favorites' }
  ];
</script>

<svelte:head>
  <title>{selectedGame ? `${selectedGame.title} — Loodation` : 'Loodation — играй в своём ритме'}</title>
</svelte:head>

<div class="app-shell">
  <aside class:mobile-open={mobileMenu} class="sidebar">
    <a class="brand" href="#home" onclick={() => go('home')} aria-label="Loodation — главная"><span class="brand-mark">L</span><span>loodation<span class="brand-dot">.</span></span></a>
    <div class="side-label">МЕНЮ</div>
    <nav class="side-nav" aria-label="Главная навигация">
      {#each nav as item}
        <button class:active={(page === item.page) || (item.page === 'catalog' && page === 'game')} onclick={() => go(item.page)}><svelte:component this={item.icon} size={19} strokeWidth={1.8} /><span>{item.label}</span>{#if item.page === 'favorites'}<span class="nav-count">2</span>{/if}</button>
      {/each}
    </nav>
    <div class="side-label collection-label">ТВОЯ КОЛЛЕКЦИЯ</div>
    <button class="collection-card" onclick={() => showNotice('Раздел коллекции скоро появится')}><span class="collection-icon">✦</span><span><b>Коллекция</b><small>Собирай достижения</small></span><ArrowRight size={16} /></button>
    <div class="sidebar-spacer"></div>
    <div class="responsible"><ShieldCheck size={16} /><span>Только игровые очки.<br />Без реальных денег.</span></div>
    <button class="profile-mini" onclick={() => go('profile')}><span class="avatar avatar-small">А</span><span class="profile-mini-copy"><b>Александр</b><small>Уровень 4 · Исследователь</small></span><ChevronDown size={15} /></button>
  </aside>

  <main class="main-area">
    <header class="topbar">
      <button class="icon-button mobile-menu" aria-label="Открыть меню" onclick={() => mobileMenu = !mobileMenu}><Menu size={21} /></button>
      <div class="crumb"><span>Игровой клуб</span>{#if page === 'game'}<ArrowRight size={14} /><b>{selectedGame?.title}</b>{:else if page === 'profile'}<ArrowRight size={14} /><b>Профиль</b>{/if}</div>
      <div class="top-actions">
        <button class="balance" onclick={() => go('profile')}><span class="coin">✦</span><span>{money(balance)}</span><span class="balance-unit">очков</span><span class="balance-plus"><Plus size={15} /></span></button>
        <button class="icon-button notification" aria-label="Уведомления" onclick={() => showNotice('Пока нет новых уведомлений')}><Bell size={19} /><i></i></button>
        <button class="avatar avatar-top" aria-label="Открыть профиль" onclick={() => go('profile')}>А</button>
      </div>
    </header>

    <div class="content">
      {#if page === 'game' && selectedGame}
        <button class="back-link" onclick={() => go('catalog')}><ArrowLeft size={16} /> К каталогу</button>
        <section class="game-detail">
          <div class="game-stage {selectedGame.tone}">
            <span class="game-glow"></span><div class="slot-machine"><div class="slot-top">LOODATION <span>✦</span></div><div class:spinning={rolling} class="reels"><span>{rolling ? '✦' : '7'}</span><span>{rolling ? '🍒' : '7'}</span><span>{rolling ? '☾' : '7'}</span></div><div class="slot-lights">✦　✧　✦　✧　✦</div></div>
            <span class="stage-decoration decoration-one">✦</span><span class="stage-decoration decoration-two">✧</span>
          </div>
          <div class="game-info"><div class="eyebrow"><span class="live-dot"></span> ДЕМО-РЕЖИМ <span class="dot-sep">·</span> {selectedGame.category.toUpperCase()}</div><h1>{selectedGame.title}</h1><p class="game-description">{selectedGame.subtitle}. Испытай удачу в демо-раунде — здесь используются только игровые очки.</p>
            <div class="game-facts"><div><small>ТВОЙ БАЛАНС</small><b><span class="coin">✦</span> {money(balance)} очков</b></div><div><small>СТАВКА РАУНДА</small><b>100 очков</b></div><div><small>ДЕМО-ВЫИГРЫШ</small><b class="positive">до 250 очков</b></div></div>
            <button class="primary-button play-button" disabled={rolling} onclick={playDemo}>{#if rolling}<span class="spinner"></span> Крутим...{:else}<Sparkles size={18} /> Играть в демо <ArrowRight size={17} />{/if}</button>
            {#if result}<div class:win={result.startsWith('Красиво')} class="round-result">{result}</div>{/if}
            <p class="fine-print"><ShieldCheck size={14} /> Игровые очки не имеют денежной стоимости</p>
          </div>
        </section>
        <section class="below-game"><div><h2>Об игре</h2><p>Лёгкий способ сделать паузу и поймать немного удачи. Результат раунда случайный и существует только в этом демо.</p></div><div class="game-tagline"><span>✦</span><b>{selectedGame.win}</b><small>демо-множитель</small></div></section>
      {:else if page === 'profile'}
        <section class="profile-page"><div class="page-kicker">ТВОЁ ПРОСТРАНСТВО</div><h1>Профиль</h1><div class="profile-hero"><div class="avatar avatar-large">А</div><div><h2>Александр</h2><p>Исследователь · в клубе с октября 2026</p><div class="level-track"><span>Уровень 4</span><div><i></i></div><small>320 / 500 XP</small></div></div><button class="quiet-button" onclick={() => showNotice('Настройки профиля скоро появятся')}><Settings2 size={16} /> Настроить</button></div>
          <div class="profile-grid"><article class="stat-card balance-stat"><div class="stat-icon"><Wallet size={19} /></div><small>ИГРОВОЙ БАЛАНС</small><strong><span class="coin">✦</span> {money(balance)}</strong><p>условных очков</p><button onclick={() => showNotice('В демо нельзя пополнять баланс')}><Plus size={15} /> Получить очки</button></article><article class="stat-card"><div class="stat-icon purple"><Crown size={19} /></div><small>ТВОЙ УРОВЕНЬ</small><strong>4</strong><p>Исследователь</p><span class="stat-note">До 5 уровня осталось 180 XP</span></article><article class="stat-card"><div class="stat-icon orange"><Flame size={19} /></div><small>СЕРИЯ В ИГРЕ</small><strong>3 <em>дня</em></strong><p>Продолжай в своём ритме</p><span class="stat-note">Лучший результат — 7 дней</span></article></div>
          <div class="activity-card"><div class="section-heading"><h2>Недавняя активность</h2><button class="text-link" onclick={() => showNotice('Это вся активность демо-профиля')}>Вся история <ArrowRight size={14} /></button></div><div class="activity-row"><span class="activity-symbol neon">✦</span><div><b>Неоновые 7</b><small>Демо-раунд · сегодня</small></div><span class="activity-result positive">+250 очков</span></div><div class="activity-row"><span class="activity-symbol dice">⚄</span><div><b>Кости судьбы</b><small>Демо-раунд · вчера</small></div><span class="activity-result">−100 очков</span></div></div>
          <p class="profile-disclaimer"><ShieldCheck size={15} /> Баланс и активность — демонстрационные данные, хранящиеся только в текущей сессии.</p></section>
      {:else}
        <section class="hero">
          <div class="hero-copy"><div class="hero-kicker">ИГРОВОЙ КЛУБ</div><h1>{#if page === 'favorites'}Твои любимые игры{:else if page === 'catalog'}Выбирай игру{:else}Играй<br />в своём ритме{/if}</h1><p>{page === 'favorites' ? 'Сохранённые игры в одном месте.' : 'Подборка мини-игр для короткой паузы. Выбирай игру и пробуй демо-раунд за условные очки.'}</p><button class="hero-button" onclick={() => document.getElementById('game-catalog')?.scrollIntoView({ behavior: 'smooth' })}>Открыть каталог <ArrowRight size={16} /></button></div>
          <div class="hero-footnote"><ShieldCheck size={14} /> Только игровые очки. Без реальных денег.</div>
        </section>
        <section id="game-catalog" class="catalog-section">
          <div class="section-heading"><div><div class="section-overline">НАХОДИ СВОЁ</div><h2>{page === 'favorites' ? 'Избранное' : 'Игры для настроения'} <span>{page === 'favorites' ? '02' : '06'}</span></h2></div><button class="text-link all-games-link" onclick={() => { page = 'catalog'; category = 'Все игры'; }}>Все игры <ArrowRight size={15} /></button></div>
          <div class="catalog-toolbar"><div class="category-tabs">{#each categories as item}<button class:selected={category === item} onclick={() => category = item}>{item}</button>{/each}</div><label class="search-box"><Search size={17} /><input bind:value={query} placeholder="Найти игру" aria-label="Найти игру" />{#if query}<button aria-label="Очистить поиск" onclick={() => query = ''}><X size={14} /></button>{/if}</label></div>
          <div class="game-grid">
            {#each (page === 'favorites' ? filteredGames.filter((game) => ['neon', 'moon'].includes(game.id)) : filteredGames) as game}
              <button class="game-card" onclick={() => openGame(game)}><div class="cover {game.tone}"><span class="cover-mark">{game.icon}</span>{#if game.tag}<span class="game-badge">{game.tag === 'ХИТ' ? 'Популярное' : 'Новинка'}</span>{/if}</div><div class="card-info"><div><strong>{game.title}</strong><small>{game.subtitle}</small></div><span class="card-arrow"><ArrowRight size={16} /></span></div><div class="card-meta"><span>{game.category}</span><span>Демо до <b>{game.win}</b></span></div></button>
            {:else}
              <div class="empty-state"><Search size={22} /><b>Таких игр пока нет</b><span>Попробуй другой запрос или категорию</span></div>
            {/each}
          </div>
          <div class="catalog-note"><span class="note-icon"><ShieldCheck size={17} /></span><span><b>Играем легко и безопасно</b><small>Здесь используются только условные игровые очки — никакой денежной ценности.</small></span><button aria-label="Подробнее о демо" onclick={() => showNotice('Это демо-каталог без денежных ставок и платежей')}><CircleHelp size={17} /></button></div>
        </section>
        <footer class="footer"><span>© 2026 Loodation</span><span><ShieldCheck size={14} /> Только развлечение · только игровые очки</span><button onclick={() => showNotice('Спасибо, что играешь ответственно')}>Играй ответственно</button></footer>
      {/if}
    </div>
  </main>
</div>

{#if mobileMenu}<button class="mobile-scrim" aria-label="Закрыть меню" onclick={() => mobileMenu = false}></button>{/if}
{#if notice}<div class="toast"><span class="toast-mark">✦</span>{notice}</div>{/if}
<nav class="bottom-nav" aria-label="Навигация"><button class:active={page === 'home'} onclick={() => go('home')}><Home size={19} /><span>Главная</span></button><button class:active={page === 'catalog' || page === 'game'} onclick={() => go('catalog')}><Compass size={19} /><span>Игры</span></button><button class:active={page === 'favorites'} onclick={() => go('favorites')}><Star size={19} /><span>Избранное</span></button><button class:active={page === 'profile'} onclick={() => go('profile')}><UserRound size={19} /><span>Профиль</span></button></nav>
