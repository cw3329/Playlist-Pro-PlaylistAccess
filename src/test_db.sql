create database if not exists PlaylistAccess;
use PlaylistAccess;

drop table if exists PlaylistAccess.UserPlaylist;
drop table if exists PlaylistAccess.User;
drop table if exists PlaylistAccess.Playlist;


create table PlaylistAccess.User (
    id varchar(36) primary key,
  	firstName varchar(30),
  	lastName varchar(30),
  	email varchar(45)
);

create table PlaylistAccess.Playlist (
  	id varchar(36) primary key,
  	name varchar(50)
);

create table PlaylistAccess.UserPlaylist (
	userId varchar(36) not null,
  	playlistId varchar(36) not null,
  	foreign key (userId) references User(id) on update cascade on delete cascade,
  	foreign key (playlistId) references Playlist(id) on update cascade on delete cascade,
  	unique key (userId, playlistId)

);

insert into PlaylistAccess.User (id, firstName, lastName, email)
values("abc", "john", "smith", "jsmith@gmail.com"),
      ("aaa", "john", "smith", "jsmith@gmail.com"),
      ("bbb", "john", "smith", "jsmith@gmail.com"),
      ("ccc", "big", "john", "bigjohn@gmail.com"),
      ("ddd", "alex", "jacobs", "alex.jacobs@gmail.com")
;

insert into PlaylistAccess.Playlist (id, name)
values ("p-abc", "rock n playlist");

insert into UserPlaylist(userId, playlistId)
values ("abc", "p-abc");