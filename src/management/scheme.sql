create table systems_meta
(
	id text not null
		constraint systems_meta_pk
			primary key,
	last_updated int not null,
	cpu_count int not null,
	cpu_freq int not null,
	cpu_perc TEXT not null,
	mem_total int not null,
	mem_available int not null,
	mem_used int not null,
	mem_free int not null,
	mem_used_perc TEXT not null,
	swap_total int not null,
	swap_used int not null,
	swap_free int not null,
	swap_used_perc text not null
);

create unique index systems_meta_id_uindex
	on systems_meta (id);

