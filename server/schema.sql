drop table if exists users;
drop table if exists photos;
create table users (
  id integer primary key autoincrement,
  username string(120) not null,
  password string(255) not null
);

create table photos (
  id integer primary key autoincrement,
  name text not null,
  file blob not null,
  creator_name string(120) not null,
  foreign key(creator_name) references users(username)
)