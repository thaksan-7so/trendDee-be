-- Sectors reference table
create table sectors (
  id serial primary key,
  code text unique not null,
  name_th text not null,
  name_en text not null,
  color text not null,
  asset_type text not null -- 'STOCK' | 'FUND' | 'FOREX' | 'ALL'
);

insert into sectors (code, name_th, name_en, color, asset_type) values
  ('AGRO',         'เกษตรและอุตสาหกรรมอาหาร', 'Agro & Food',          '#16A34A', 'STOCK'),
  ('CONSUMP',      'สินค้าอุปโภคบริโภค',       'Consumer Products',    '#D97706', 'STOCK'),
  ('FINCIAL',      'การเงิน',                  'Financials',           '#2563EB', 'STOCK'),
  ('INDUS',        'อุตสาหกรรม',               'Industrials',          '#7C3AED', 'STOCK'),
  ('PROPCON',      'อสังหาริมทรัพย์',           'Property & Const.',   '#DC2626', 'STOCK'),
  ('RESOURC',      'ทรัพยากร',                 'Resources',            '#B45309', 'STOCK'),
  ('SERVICE',      'บริการ',                   'Services',             '#0891B2', 'STOCK'),
  ('TECH',         'เทคโนโลยี',                'Technology',           '#6366F1', 'STOCK'),
  ('FUND_EQUITY',  'กองทุนหุ้น',               'Equity Fund',          '#6366F1', 'FUND'),
  ('FUND_FIXED',   'กองทุนตราสารหนี้',          'Fixed Income Fund',    '#0EA5E9', 'FUND'),
  ('FUND_MIXED',   'กองทุนผสม',                'Balanced Fund',        '#8B5CF6', 'FUND'),
  ('FUND_REIT',    'กองทุน REITs',             'REITs Fund',           '#F59E0B', 'FUND'),
  ('FUND_GLOBAL',  'กองทุนต่างประเทศ',          'Global Fund',          '#EC4899', 'FUND'),
  ('FUND_MONEY',   'กองทุนตลาดเงิน',            'Money Market',         '#14B8A6', 'FUND'),
  ('FX_MAJOR',     'สกุลเงินหลัก',             'Major Pairs',          '#64748B', 'FOREX'),
  ('FX_ASIA',      'สกุลเงินเอเชีย',           'Asian Currencies',     '#F97316', 'FOREX'),
  ('FX_COMMODITY', 'Commodity Currencies',     'Commodity FX',         '#84CC16', 'FOREX');

-- Assets master table
create table assets (
  id uuid primary key default gen_random_uuid(),
  symbol text unique not null,
  name_th text not null,
  asset_type text not null,
  sector_code text references sectors(code),
  metadata jsonb default '{}',
  updated_at timestamptz default now()
);

-- News articles
create table news_articles (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  url text unique not null,
  source text not null,
  content text,
  published_at timestamptz not null,
  sector_codes text[] default '{}',
  ticker_mentions text[] default '{}',
  created_at timestamptz default now()
);

create index on news_articles (published_at desc);
create index on news_articles using gin (sector_codes);

-- Daily AI summaries
create table daily_summaries (
  id uuid primary key default gen_random_uuid(),
  date date unique not null,
  summary_text text not null,
  market_sentiment text not null,
  created_at timestamptz default now()
);

-- Stock picks from AI
create table stock_picks (
  id uuid primary key default gen_random_uuid(),
  date date not null,
  ticker text not null,
  asset_type text not null,
  sector_code text,
  action text not null,
  reasoning text not null,
  confidence float not null,
  created_at timestamptz default now()
);

create index on stock_picks (date desc, ticker);

-- Portfolio transactions
create table portfolio_transactions (
  id uuid primary key default gen_random_uuid(),
  asset_id uuid references assets(id),
  symbol text not null,
  name_th text,
  asset_type text not null,
  sector_code text,
  action text not null,
  quantity float not null,
  price float not null,
  transaction_date date not null,
  notes text,
  created_at timestamptz default now()
);

create index on portfolio_transactions (transaction_date desc);
