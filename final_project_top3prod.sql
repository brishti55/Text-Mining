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
select count(uniquesentid) from top3_wordorient where polarity='negative'; --9206update top3prod
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


select distinct uniquesentid,
  case 
  when polarity = 'positive' then 'non-negative'
  when polarity='neutral' then 'non-negative'
    else 'negative'
  end as polarity
  from top3_wordorient
  order by uniquesentid desc;

select count(uniquesentid) from top3_wordorient where polarity='neutral'; -- 251474

--drop table top3_class;
--Create class as negative and non-negative for top 3 products
create table top3_class as
select distinct uniquesentid,
  case 
  when polarity = 'positive' then 'non-negative'
  when polarity='neutral' then 'non-negative'
    else 'negative'
  end as polarity
  from top3_wordorient
  order by uniquesentid desc;

select count(uniquesentid) from top3_class where polarity='negative'; --7554
select count(uniquesentid) from top3_class where polarity='non-negative'; -- (37030-7456)= 29574

select * from top3_class;

DELETE FROM top3_class
WHERE rowid not in
(SELECT MIN(rowid)
FROM top3_class
GROUP BY uniquesentid); --7456 duplicates

-- Join the class with wordlist to be used with the pivot function
create table top3_classjoin as
select top3_class.uniquesentid as id, word, top3_class.polarity as class from top3_class join top3_wordorient on (top3_class.uniquesentid=top3_wordorient.uniquesentid);

select count(distinct id) from top3_classjoin where class='negative'; --7554

create table top3_neg_wordlist as
select id, word, class from top3_classjoin where class = 'negative';

select count(distinct id) from top3_neg_wordlist; --7554

create table top3_nonneg_wordlist as
select id, word, class from top3_classjoin where class = 'non-negative';

select count(distinct id) from top3_nonneg_wordlist; --29574

-- This table is actually not necessary
--drop table top3_int_1;
-- create table top3_int_1 as
select top3_neg_wordlist.id, top3_neg_wordlist.word, top3df.df 
  from top3_neg_wordlist join top3df 
    on (top3df.word = top3_neg_wordlist.word) 
order by top3df.df desc;

--create table top3_int1 as
select word, count(distinct id) as total from top3_neg_wordlist
group by word
order by total desc;

select count(uniquesentid) from top3_class; --total 37128 where neg 7554, non-neg 29574

--Table for calculating P(Class|Term) where P(c|t)=Number of sentences in class with term/ total number of sentences with term
--drop table classneg_pct;
--create table top3_pct as 
select top3_int1.word, total, df, (df/37128) as pt, (top3_int1.total/top3df.df) as pct from top3_int1 join top3df on (top3df.word = top3_int1.word)
where top3df.df>3 and top3df.df<3000
order by df desc;

select count(word) from top3_pct; --4285

--drop table top3_int2;
--create table top3_int2 as 
select top3_int1.word, (7554-top3_int1.total) as total_withoutterm, (37128-top3df.df) as total_df_withoutterm
from top3_int1 join top3df on (top3df.word = top3_int1.word)
where top3df.df>3 and top3df.df<3000
order by df desc;

select count(word) from top3_int2; --4285

--Table for calculating P(Class|Not Term) where P(c|nt)=Number of sentences in class without the term/ total number of sentences without the term
--drop table top3_pcnt;
--create table top3_pcnt as
select word, (total_withoutterm/total_df_withoutterm) as pcnt from top3_int2
order by pcnt desc;

select count(word) from top3_pcnt; --4285

--drop table top3_int3;
--create table top3_int3 as
select top3_pct.word, (-1)*((7554/37128)*(log(10,(7554/37128)))) as part1, 
(top3_pct.pt*top3_pct.pct*(log(10,top3_pct.pct))) as part2, 
(1-top3_pct.pt)*top3_pcnt.pcnt*(log(10,top3_pcnt.pcnt)) as part3 
from top3_pct join top3_pcnt on (top3_pct.word = top3_pcnt.word);

--final ig calculation
--drop table classneg_ig;
--create table top3_ig as
select word, (part1+part2+part3) as finalig from top3_int3
order by finalig desc;

select * from top3_ig where rownum <= 500;

--for top 200 words
create table top3_ig200 as select * from 
  (select distinct id, class, word from top3_classjoin) 
    pivot 
    (count(word) for word in ('pressure','problem','problems','bad','drown','hard','block','noisy','annoying','noises','disappointed','trouble','blocks','stuck','difficult','lowest','leave','noise','broke','stop','stopped','hate','wrong','drowns','leak','neighbors','best','falling','prevent','pain','pay','mess','blocking','sleeping','avoid','love','protein','great','useless','waste','bother','setting','alone','tired','weird','horrible','skeptical','button','outside','worse','negative','empty','lost','asleep','terrible','died','cut','loud','enough','unwanted','weak','handle','failed','doubt','missed','poor','lack','snoring','crazy','broken','worry','worst','alarm','worried','leaked','get','sleep','sore','regret','nasty','completely','even','people','dogs','hated','sounds','hurt','sorry','barking','odd','limited','sick','crap','neighbor','pleased','downside','forget','complained','afraid','stops','tastes','gross','dead','drop','getting','highly','food','good','might','without','chocolate','still','complain','awkward','damage','screaming','blocked','upset','miss','lazy','drowned','loose','admit','trapped','house','flossing','milk','floss','cancel','fire','fail','hesitant','flow','dial','time','awful','mistake','irritating','disturbing','disturbed','strange','uncomfortable','hesitate','would','cutting','disappointing','mixes','areas','hose','reach','loss','fake','warning','fall','recommend','solved','street','gum','due','turn','sometimes','help','crying','missing','ugly','cuts','obnoxious','whey','around','better','background','extraneous','dump','disturb','attention','little','anything','remove','live','trying','bleeding','door','either','driving','hide','ringing','leaking','easy','traffic','nutrition','back','clock','never','could','night','working','bitter','nervous','hear','suffer'));

--for top 500 words
create table top3_ig500 as select * from 
  (select distinct id, class, word from top3_classjoin) 
    pivot 
    (count(word) for word in ('pressure','problem','problems','bad','drown','hard','block','noisy','annoying','noises','disappointed','trouble','blocks','stuck','difficult','lowest','leave','noise','broke','stop','stopped','hate','wrong','drowns','leak','neighbors','best','falling','prevent','pain','pay','mess','blocking','sleeping','avoid','love','protein','great','useless','waste','bother','setting','alone','tired','weird','horrible','skeptical','button','outside','worse','negative','empty','lost','asleep','terrible','died','cut','loud','enough','unwanted','weak','handle','failed','doubt','missed','poor','lack','snoring','crazy','broken','worry','worst','alarm','worried','leaked','get','sleep','sore','regret','nasty','completely','even','people','dogs','hated','sounds','hurt','sorry','barking','odd','limited','sick','crap','neighbor','pleased','downside','forget','complained','afraid','stops','tastes','gross','dead','drop','getting','highly','food','good','might','without','chocolate','still','complain','awkward','damage','screaming','blocked','upset','miss','lazy','drowned','loose','admit','trapped','house','flossing','milk','floss','cancel','fire','fail','hesitant','flow','dial','time','awful','mistake','irritating','disturbing','disturbed','strange','uncomfortable','hesitate','would','cutting','disappointing','mixes','areas','hose','reach','loss','fake','warning','fall','recommend','solved','street','gum','due','turn','sometimes','help','crying','missing','ugly','cuts','obnoxious','whey','around','better','background','extraneous','dump','disturb','attention','little','anything','remove','live','trying','bleeding','door','either','driving','hide','ringing','leaking','easy','traffic','nutrition','back','clock','never','could','night','working','bitter','nervous','hear','suffer','annoyance','ear','delicious','cause','mad','losing','disgusting','reservoir','bothered','ambient','going','tinnitus','unit','damn','place','etc','dont','start','stupid','restless','control','annoyed','inconsiderate','risk','inconvenient','sad','terribly','shoot','voices','keep','minor','kind','bit','helps','settings','especially','effectively','sound','higher','machine','area','seemed','stomach','music','became','disappointment','hell','shame','irritated','sprung','challenge','frustrated','fear','silly','forced','gag','nuts','price','something','neighborhood','excellent','gums','always','cars','starts','staying','apartment','cancer','surrounding','slightly','solve','swear','happy','dirt','failure','anxious','choke','suspect','die','sucks','prevents','hurts','hates','wasting','inflamed','distracted','ridiculous','end','press','caused','gets','read','really','bothers','awake','places','upstairs','waking','motor','exactly','making','thing','hunger','ill','warned','else','leakage','talking','accidentally','criticism','warn','harsh','kill','struggling','frustrating','unhappy','severe','annoy','fails','error','plastic','may','constant','since','somewhat','unless','gold','despite','hours','car','someone','becoming','external','quiet','properly','want','seem','living','temporarily','wow','emergency','solves','alert','dirty','bothersome','dreaded','cancels','avoided','disruptive','death','scared','suffers','costly','cry','fatigue','hiding','ignore','badly','distraction','drunk','wasted','way','vanilla','flavor','heart','dropped','leaks','optimum','plaque','favorite','convinced','causing','frequency','lasts','trucks','variable','coming','find','aftertaste','roommates','grew','mind','normal','push','add','satisfied','possible','serving','pipes','make','advertised','pump','increase','spots','mornings','sufficient','bacteria','dislike','chronic','exposed','shocked','disappoint','conversations','charged','insane','frustration','worrying','unsure','screams','ghost','struggle','distract','dread','kills','defect','preventing','cries','worthless','distracts','fool','regrets','rendering','bored','washer','worn','suffering','interrupted','loudly','sirens','within','sensitive','glad','works','dissolves','thank','per','fixed','otherwise','seal','ice','cat','double','fact','usually','old','middle','think','banana','however','quite','mean','explain','outdoor','highest','inside','periodontal','wake','holding','company','wisdom','stream','results','quality','pause','months','simply','drove','split','speeds','throat','voice','pressed','sorts','mention','playing','dog','worth','frozen','developed','hit','head','particles','found','serious','initially','silence','pockets','removing','knocked','drives','unbelievable','guilty','first','hearing','went','assembly','garbage','swears','alas','excuse'));