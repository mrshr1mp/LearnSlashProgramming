-- The database behind accounts and friends (Supabase project "learnslashprogramming").
-- Already applied. Kept here so the privacy rules are written down and can be rebuilt.
--
-- Who can see what (enforced by Postgres row-level security, not by the app):
--   * strangers and signed-out users: nothing
--   * accepted friends: your profile, finished missions and daily activity
--   * your code for a mission: only friends who have finished that mission too

-- ===== tables =====
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  username text not null check (username ~ '^[A-Za-z0-9_]{3,20}$'),
  created_at timestamptz not null default now()
);
create unique index profiles_username_lower on public.profiles (lower(username));

create table public.friendships (
  requester uuid not null references public.profiles(id) on delete cascade,
  addressee uuid not null references public.profiles(id) on delete cascade,
  status text not null default 'pending' check (status in ('pending', 'accepted')),
  created_at timestamptz not null default now(),
  primary key (requester, addressee),
  check (requester <> addressee)
);
create index friendships_addressee on public.friendships (addressee);

create table public.completions (
  user_id uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  track text not null check (track ~ '^[a-z0-9_-]{1,40}$'),
  mission_id text not null check (mission_id ~ '^[A-Za-z0-9_-]{1,60}$'),
  xp int not null check (xp between 0 and 1000),
  completed_on date not null,
  primary key (user_id, track, mission_id)
);

create table public.activity (
  user_id uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  day date not null,
  checks int not null check (checks between 0 and 10000),
  primary key (user_id, day)
);

create table public.solutions (
  user_id uuid not null default auth.uid(),
  track text not null,
  mission_id text not null,
  filename text not null check (filename ~ '^[A-Za-z0-9_.-]{1,60}$'),
  code text not null check (octet_length(code) <= 100000),
  updated_at timestamptz not null default now(),
  primary key (user_id, track, mission_id),
  -- code can only exist for a mission its owner has completed
  foreign key (user_id, track, mission_id) references public.completions (user_id, track, mission_id) on delete cascade
);

-- ===== helpers =====
create schema if not exists private;  -- not exposed through the API
revoke all on schema private from public, anon;
grant usage on schema private to authenticated;

create function private.is_friend(other uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (
    select 1 from public.friendships f
    where f.status = 'accepted'
      and ((f.requester = (select auth.uid()) and f.addressee = other)
        or (f.addressee = (select auth.uid()) and f.requester = other)));
$$;

create function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, username) values (new.id, new.raw_user_meta_data ->> 'username');
  return new;
end;
$$;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

create function public.username_available(name text) returns boolean
language sql stable security definer set search_path = '' as $$
  select name ~ '^[A-Za-z0-9_]{3,20}$'
     and not exists (select 1 from public.profiles p where lower(p.username) = lower(name));
$$;

create function public.send_friend_request(target text) returns text
language plpgsql security definer set search_path = '' as $$
declare
  me uuid := auth.uid();
  them uuid;
begin
  if me is null then raise exception 'Not signed in'; end if;
  select id into them from public.profiles where lower(username) = lower(target);
  if them is null then raise exception 'No user called %', target; end if;
  if them = me then raise exception 'That''s you!'; end if;
  if exists (select 1 from public.friendships where requester = them and addressee = me) then
    update public.friendships set status = 'accepted' where requester = them and addressee = me;
    return 'accepted';
  end if;
  insert into public.friendships (requester, addressee) values (me, them) on conflict do nothing;
  return 'sent';
end;
$$;

create function public.accept_friend(requester_name text) returns void
language plpgsql security definer set search_path = '' as $$
begin
  update public.friendships f set status = 'accepted'
  from public.profiles p
  where p.id = f.requester and lower(p.username) = lower(requester_name) and f.addressee = auth.uid();
end;
$$;

-- ===== permissions =====
revoke all on public.profiles, public.friendships, public.completions, public.activity, public.solutions from anon;
revoke execute on function private.is_friend(uuid), public.handle_new_user(), public.username_available(text),
  public.send_friend_request(text), public.accept_friend(text) from public, anon, authenticated;
grant execute on function private.is_friend(uuid), public.send_friend_request(text), public.accept_friend(text) to authenticated;
grant execute on function public.username_available(text) to anon, authenticated;

alter table public.profiles enable row level security;
alter table public.friendships enable row level security;
alter table public.completions enable row level security;
alter table public.activity enable row level security;
alter table public.solutions enable row level security;

create policy "see self and connections" on public.profiles for select to authenticated using (
  id = (select auth.uid()) or exists (
    select 1 from public.friendships f
    where (f.requester = (select auth.uid()) and f.addressee = profiles.id)
       or (f.addressee = (select auth.uid()) and f.requester = profiles.id)));

-- creating and accepting requests only happens through the functions above,
-- so nobody can write themselves into someone else's friend list
create policy "see own friendships" on public.friendships for select to authenticated
  using ((select auth.uid()) in (requester, addressee));
create policy "remove own friendships" on public.friendships for delete to authenticated
  using ((select auth.uid()) in (requester, addressee));

create policy "read own or friends" on public.completions for select to authenticated
  using (user_id = (select auth.uid()) or private.is_friend(user_id));
create policy "insert own" on public.completions for insert to authenticated with check (user_id = (select auth.uid()));
create policy "update own" on public.completions for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
create policy "delete own" on public.completions for delete to authenticated using (user_id = (select auth.uid()));

create policy "read own or friends" on public.activity for select to authenticated
  using (user_id = (select auth.uid()) or private.is_friend(user_id));
create policy "insert own" on public.activity for insert to authenticated with check (user_id = (select auth.uid()));
create policy "update own" on public.activity for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
create policy "delete own" on public.activity for delete to authenticated using (user_id = (select auth.uid()));

create policy "read own, or friends who finished it" on public.solutions for select to authenticated using (
  user_id = (select auth.uid())
  or (private.is_friend(user_id) and exists (
    select 1 from public.completions c
    where c.user_id = (select auth.uid()) and c.track = solutions.track and c.mission_id = solutions.mission_id)));
create policy "insert own" on public.solutions for insert to authenticated with check (user_id = (select auth.uid()));
create policy "update own" on public.solutions for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
create policy "delete own" on public.solutions for delete to authenticated using (user_id = (select auth.uid()));
