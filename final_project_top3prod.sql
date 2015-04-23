update top3prod
set prodid = 1
where prodid='B000GLRREU';

update top3prod
set prodid = 2
where prodid='B000KUHFGM';

update top3prod
set prodid = 3
where prodid='B000QSNYGI';

select count(word) from top3prod where regexp_like (word, '^[''0-9]'); --7019 12563

delete from top3prod where word like '%''%'; --10971
delete from top3prod where word is null;
delete from top3prod where not regexp_like (word, '^[a-z]'); --delete special characters

delete from top3prod where length(word) <3 and word not like 'a+' and word not like 'ok'; --word with two characters except a+ and ok

delete from top3prod 
  where regexp_like (word, '^[''0-9]') or word like '%.%' or word like '%''%'; --delete all columns for seperate conditions

select count(distinct word) from top3prod; -- total number of reviews 7838, 290589 sentences in total, 13953 distinct words

create table top3df as
select word, count(reviewid) as DF
from top3prod
group by word
ORDER BY df desc;

select count(word) from top3df; --13953

create table top3_wordorient as
select concat(reviewid, sentid) as uniquesentid, wordid, word, afin_vocb.polarity
  from top3prod left join afin_vocb on (afin_vocb.term = top3prod.word);

update top3_wordorient
set polarity = 'neutral'
where polarity is null;

select count(uniquesentid) from top3_wordorient where polarity='positive'; --29909 
select count(uniquesentid) from top3_wordorient where polarity='negative'; --9206
select count(uniquesentid) from top3_wordorient where polarity='neutral'; -- 251474