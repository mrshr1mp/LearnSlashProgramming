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

-- ===== profile pictures =====
-- a small picture stored as a data URL (the app resizes it to 128x128); only raster formats, max ~60 KB
alter table public.profiles add column avatar text check (
  avatar is null or (length(avatar) <= 60000 and avatar ~ '^data:image/(png|jpeg|webp);base64,[A-Za-z0-9+/]+=*$'));

-- you may change your own picture, and nothing else about your profile
revoke insert, update, delete on public.profiles from authenticated;
grant update (avatar) on public.profiles to authenticated;
create policy "update own avatar" on public.profiles for update to authenticated
  using (id = (select auth.uid())) with check (id = (select auth.uid()));

-- ===== course marketplace =====
-- Players can only read published courses; only the maintainer publishes (tools/publish_course.py + SQL).
create table public.courses (
  id text primary key check (id ~ '^[a-z0-9_-]{1,40}$' and id <> 'courses'),
  name text not null,
  description text not null default '',
  logo text not null default '',
  version int not null default 1,
  missions int not null default 0,
  chapters text[] not null default '{}',
  published boolean not null default false,
  updated_at timestamptz not null default now()
);

create table public.course_files (
  course_id text not null references public.courses(id) on delete cascade,
  -- relative paths only: no leading slash, no "..", just safe characters
  path text not null check (path ~ '^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*$' and path !~ '(^|/)\.\.(/|$)'),
  content text not null check (octet_length(content) <= 200000),
  primary key (course_id, path)
);

revoke all on public.courses, public.course_files from anon;
revoke insert, update, delete on public.courses, public.course_files from authenticated;
alter table public.courses enable row level security;
alter table public.course_files enable row level security;

create policy "signed-in users see published courses" on public.courses for select to authenticated
  using (published);
create policy "signed-in users download published courses" on public.course_files for select to authenticated
  using (exists (select 1 from public.courses c where c.id = course_files.course_id and c.published));

-- ===== course publishers =====
-- Only accounts in private.publishers can publish (tools/publish_course.py calls these).
create table private.publishers (user_id uuid primary key references auth.users(id) on delete cascade);
revoke all on private.publishers from public, anon, authenticated;
insert into private.publishers (user_id) select id from public.profiles where username = 'Jksn';

create function private.require_publisher() returns void
language plpgsql security definer set search_path = '' as $$
begin
  if not exists (select 1 from private.publishers where user_id = auth.uid()) then
    raise exception 'Only course publishers can do this';
  end if;
end;
$$;

-- 1. start: save the course details, hide it, and clear its old files
create function public.begin_publish(course text, info jsonb) returns void
language plpgsql security definer set search_path = '' as $$
begin
  perform private.require_publisher();
  insert into public.courses (id, name, description, logo, missions, chapters, published, version)
  values (course, info ->> 'name', coalesce(info ->> 'description', ''), coalesce(info ->> 'logo', ''),
          (info ->> 'missions')::int, array(select jsonb_array_elements_text(info -> 'chapters')), false, 0)
  on conflict (id) do update set name = excluded.name, description = excluded.description, logo = excluded.logo,
    missions = excluded.missions, chapters = excluded.chapters, published = false;
  delete from public.course_files where course_id = course;
end;
$$;

-- 2. upload files in batches: [{"path": ..., "content": ...}, ...] (the table's checks still apply)
create function public.publish_course_files(course text, files jsonb) returns int
language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  perform private.require_publisher();
  insert into public.course_files (course_id, path, content)
  select course, f ->> 'path', f ->> 'content' from jsonb_array_elements(files) f
  on conflict (course_id, path) do update set content = excluded.content;
  get diagnostics n = row_count;
  return n;
end;
$$;

-- 3. finish: show it again with a new version number, so everyone sees "Update"
create function public.finish_publish(course text) returns int
language plpgsql security definer set search_path = '' as $$
declare v int;
begin
  perform private.require_publisher();
  update public.courses set published = true, version = version + 1, updated_at = now() where id = course returning version into v;
  return v;
end;
$$;

revoke execute on function private.require_publisher(), public.begin_publish(text, jsonb),
  public.publish_course_files(text, jsonb), public.finish_publish(text) from public, anon;
grant execute on function private.require_publisher(), public.begin_publish(text, jsonb),
  public.publish_course_files(text, jsonb), public.finish_publish(text) to authenticated;
