drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username string(120) not null,
  password string(255) not null
);

create table photos (
  id integer primary key autoincrement,
  name text not null,
  creator_id integer not null,
  foreign key(creator_id) references users(id)
)