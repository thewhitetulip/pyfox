select guid from moz_places;

select url, moz_places.title, rev_host, frecency, last_visit_date from moz_places  join  moz_bookmarks on moz_bookmarks.fk=moz_places.id
where moz_places.url  like 'http%' and visit_count>0;

select url, moz_places.title, rev_host, frecency, last_visit_date from moz_places  where title is null group by rev_host
having moz_places.url like 'http%' order by count(*) 


select * from moz_places  join  moz_bookmarks on moz_bookmarks.fk=moz_places.id
where moz_places.url  like 'http%';

select min(dateAdded) from  moz_bookmarks join moz_places on moz_bookmarks.fk=moz_places.id
where moz_places.url  like 'http%';


select rev_host, frecency from moz_places group by rev_host order by frecency desc ;

select url, title, last_visit_date  from moz_historyvisits natural join moz_places where url  like '%http%' order by visit_date desc;

select url, title, last_visit_date,rev_host  from moz_historyvisits natural join moz_places where url  like '%http%' and last_visit_date is not null
 order by last_visit_date desc;
 
 select * from moz_historyvisits natural join moz_places;
