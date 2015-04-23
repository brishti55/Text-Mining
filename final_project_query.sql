select count(reviewID) from topprod1ns; --total number of reviews 3270, total number of sentences 15389

--delete from topprod1ns where regexp_like (word, '^[0-9]') and word not like '%''%';
--drop table temporary;
--create table temporary as 
--select concat(reviewID, sentID) as uniqueSentID from topprod1ns;

--select count(distinct uniquesentid) from temporary;
--select count(reviewID) from topprod1s;

--DF table
--create table topProd1NS_DF as
select word, count(distinct reviewid) as DF
from topprod1ns
where regexp_like (word, '^[a-z]') and word not like '%''%' and word not like '%.%' -- single quote is escaped by doubling it
group by word
ORDER BY count(distinct reviewid) desc;

select count(word) from topprod1ns_df; --7927 unique terms

--count the number of positive and negative terms in AFIN list
select count(term) from afin_vocab
where valence < 0; --total 878 positive terms and 1598 negative terms in the vocubulary list

--decide the polarity of the terms
--drop table afin_vocb;
--create table AFIN_VOCB as
select term, valence, 
  case 
    when valence > 0 then 'positive'
    else 'negative'
  end as polarity
  from afin_org
  order by valence desc; 


--drop table wordOrient;
--create table wordOrient as
select concat(reviewID, sentID) as uniqueSentID, wordID, word, afin_vocb.polarity 
from topprod1ns left join afin_vocb on (afin_vocb.term=topprod1ns.word)
where regexp_like (word, '^[a-z]') and word not like '%''%' and word not like '%.%';

select count(distinct uniqueSentID) from wordorient; -- unique sentences 15380

update wordorient
set polarity = 'non-positive'
where polarity is null;

  
--create table wordorientnew as
select * from wordorient;

--changed all non-positive to positive as they don't change overall polarity
update wordorientnew
set polarity = 'positive'
where polarity = 'non-positive';

--3249 sentences with both positive and negative words (cumulated polarity is calculated as negative)
--drop table intpolarity;
--create table intpolarity as
select distinct uniquesentid, polarity,
  case 
    when polarity = 'positive'
      then 'positive'
    else 'negative'
  end as cumulative_polarity
  from wordorientnew
  order by uniquesentid;
  
select count(distinct uniqueSentID) from intpolarity; --15380

select count(distinct uniqueSentID) from wordorient --8313
  where polarity = 'positive';

select count(distinct uniqueSentID) from wordorient 
  where polarity = 'non-positive'; --15130

select count(distinct uniqueSentID) from wordorient
  where polarity = 'negative'; --3249
  
--create table wordorientnew as
select count(distinct uniqueSentID) from intpolarity --total 15380, negative 3249
where polarity = 'positive';

--drop table pos_terms;
--create table pos_terms as
--select uniquesentid as id, polarity from intpolarity;

delete from pos_terms where id in ( 
select id from
( select  id, polarity, row_number() over ( partition by id order by id, polarity asc) row_num 
  from pos_terms
) where row_num >1
);

delete from pos_terms where polarity = 'negative';


select count(distinct id) from pos_terms where polarity = 'positive'; --49 (deleted 3200 + 49 = 3249 total negative)

--UPDATE t1
--   SET id = sequence_name.nextval;
   
--ALTER TABLE t1
--  ADD CONSTRAINT t1_id PRIMARY KEY(id)
--
--CREATE TRIGGER new_trigger
--  BEFORE INSERT ON t1
--  FOR EACH ROW
--BEGIN
--  :new.id := sequence_name.nextval;
--END;

--create table neg_terms as 
select uniquesentid as id, polarity from intpolarity
where polarity = 'negative';

select count(distinct id) from neg_terms; -- 3249 neg
select count(distinct id) from pos_terms; -- 12131

--check how many sentences have both positive and negative
select uniquesentid as id, count(polarity)as polarity from intpolarity
group by uniquesentid
order by polarity desc;



