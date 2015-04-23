--Final Project Part-2, 1 Product, class negative and non-negative

select count(distinct uniquesentid) from wordorientnew;

--join words table with vocabulary table and decide polarity
--create table wordjoin as
select concat(reviewID, sentID) as uniqueSentID, wordID, word, 
Case when afin_vocb.term is null then 1 else 0 end as noPolarity,
Case when (polarity = 'positive') then 1 else 0 end as isPositive,
Case when (polarity = 'negative') then 1 else 0 end as isNegative
FROM topprod1ns
LEFT JOIN afin_vocb ON topprod1ns.word=afin_vocb.term;

select count(distinct uniqueSentID) from wordjoin
where regexp_like (word, '^[a-z]'); --15380

delete from wordjoin where not regexp_like (word, '^[a-z]');

select count(distinct uniquesentid) from wordjoin --positive 8313, negative 3249, nopolarity 15130
where nopolarity=1;

--create table class_neg as
select distinct uniquesentid,
case when (nopolarity+isPositive)=1 then 'non-negative' else '0' end as non_negative,
case when isnegative=1 then 'negative' else '0' end as negative 
from wordjoin
order by uniquesentid;

select count(distinct uniquesentid) from class_neg where negative='negative' and non_negative='0';

--drop table test_polarity;
--create table test_polarity as
select uniquesentid as id, 
case when polarity='positive' then 'non-negative' else 'negative' end as class
from intpolarity
order by uniquesentid;

-- Delete duplicate values with negative and non-negative while keeping the negative
DELETE FROM test_polarity
WHERE rowid not in
(SELECT MIN(rowid)
FROM test_polarity
GROUP BY id);

select count(id) from test_polarity where class='non-negative';

create table class_join as
select test_polarity.id, word, test_polarity.class from test_polarity join wordorientnew on (test_polarity.id=wordorientnew.uniquesentid);

select count(distinct id) from class_join where class='negative'; --3249

--create table classneg_int_1 as 
select neg_wordlist.id, word, df from neg_wordlist join topprod1ns_df using(word)
order by topprod1ns_df.df desc;

--create table classneg_int_2 as
select word, count(distinct id) as total from classneg_int_1
group by word
order by total desc;

--Table for calculating P(Class|Term) where P(c|t)=Number of sentences in class with term/ total number of sentences with term
--drop table classneg_pct;
--create table classneg_pct as 
select classneg_int_2.word, total, df, (df/15380) as pt, (classneg_int_2.total/topprod1ns_df.df) as pct from classneg_int_2 join topprod1ns_df on (topprod1ns_df.word = classneg_int_2.word)
where length(topprod1ns_df.word)>1
order by pct desc;

select count(word) from classneg_pct; --4394

--drop table classneg_int_3;
--create table classneg_int_3 as 
select classneg_int_2.word, (3249-classneg_int_2.total) as total_withoutterm, (15380-topprod1ns_df.df) as total_df_withoutterm
from classneg_int_2 join topprod1ns_df on (topprod1ns_df.word = classneg_int_2.word)
where length(classneg_int_2.word)>1
order by total_df_withoutterm desc;

select count(word) from classneg_int_3; --4394

--Table for calculating P(Class|Not Term) where P(c|nt)=Number of sentences in class without the term/ total number of sentences without the term
--drop table classneg_pcnt;
--create table classneg_pcnt as
select word, (total_withoutterm/total_df_withoutterm) as pcnt from classneg_int_3
order by pcnt desc;

select count(word) from classneg_pcnt; -- 4394

--drop table classneg_int_4;
--create table classneg_int_4 as
select classneg_pct.word, (-1)*((12131/15380)*(log(10,(12131/15380)))) as part1, 
(classneg_pct.pt*classneg_pct.pct*(log(10,classneg_pct.pct))) as part2, 
(1-classneg_pct.pt)*classneg_pcnt.pcnt*(log(10,classneg_pcnt.pcnt)) as part3 
from classneg_pct join classneg_pcnt on (classneg_pct.word = classneg_pcnt.word);

--final ig calculation
--drop table classneg_ig;
--create table classneg_ig as
select word, (part1+part2+part3) as finalig from classneg_int_4
order by finalig desc;

-- top 200 terms
select * from classneg_ig where rownum <=200;

--top 500 terms
select * from classneg_ig where rownum <=500;

--'pressure','problems','problem','hard','bad','stuck','broke','leak','difficult','stopped','stop','hate','disappointed','mess','pain','button','leave','noisy','prevent','useless','handle','love','failed','empty','wrong','leaked','missed','annoying','negative','died','lowest','weak','alone','trouble','water','setting','avoid','broken','control','high','pay','flow','dial','food','highly','hurt','trapped','poor','best','awkward','pleased','waste','stops','damage','hated','get','floss','flossing','lack','lost','loose','turn','great','settings','reach','worse','hose','miss','bother','uncomfortable','cut','product','remove','start','complained','lazy','sorry','leaking','bleeding','recommend','gum','forget','fail','regret','adjustable','worry','even','working','variable','lower','areas','months','getting','easy','anything','limited','sore','tired','shoot','worried','warning','dump','disappointing','enough','reservoir','might','back','still','starts','people','wo','within','adjust','higher','cutting','skeptical','gross','sprung','missing','doubt','press','always','gets','read','place','first','places','drop','hesitate','failure','inflamed','admit','mistake','dont','highest','plastic','price','make','motor','later','end','unless','criticism','afraid','dirt','dead','hesitant','inconvenient','complain','hurts','downside','slightly','leakage','either','eventually','gums','became','caused','cause','increase','without','little','heart','small','time','around','thing','cancer','could','risk','fails','annoyance','worst','terrible','silly','irritated','crap','low','happy','especially','overall','leaks','spots','works','despite','way','found','properly','strong','sometimes','plaque','fixed','causing','max','area','unit','putting','disappointment','accidentally','shame'

--'pressure','problems','problem','hard','bad','stuck','broke','leak','difficult','stopped','stop','hate','disappointed','mess','pain','button','leave','noisy','prevent','useless','handle','love','failed','empty','wrong','leaked','missed','annoying','negative','died','lowest','weak','alone','trouble','water','setting','avoid','broken','control','high','pay','flow','dial','food','highly','hurt','trapped','poor','best','awkward','pleased','waste','stops','damage','hated','get','floss','flossing','lack','lost','loose','turn','great','settings','reach','worse','hose','miss','bother','uncomfortable','cut','product','remove','start','complained','lazy','sorry','leaking','bleeding','recommend','gum','forget','fail','regret','adjustable','worry','even','working','variable','lower','areas','months','getting','easy','anything','limited','sore','tired','shoot','worried','warning','dump','disappointing','enough','reservoir','might','back','still','starts','people','wo','within','adjust','higher','cutting','skeptical','gross','sprung','missing','doubt','press','always','gets','read','place','first','places','drop','hesitate','failure','inflamed','admit','mistake','dont','highest','plastic','price','make','motor','later','end','unless','criticism','afraid','dirt','dead','hesitant','inconvenient','complain','hurts','downside','slightly','leakage','either','eventually','gums','became','caused','cause','increase','without','little','heart','small','time','around','thing','cancer','could','risk','fails','annoyance','worst','terrible','silly','irritated','crap','low','happy','especially','overall','leaks','spots','works','despite','way','found','properly','strong','sometimes','plaque','fixed','causing','max','area','unit','putting','disappointment','accidentally','shame','warn','washer','frustration','prevents','mad','weird','hell','suspect','point','bacteria','cold','stream','pump','serious','company','holding','ultra','bit','removing','increased','good','constant','realize','switch','sufficient','wisdom','fresh','better','kind','periodontal','went','seemed','falling','dropped','temporarily','attention','excellent','wow','though','worthless','fire','anxious','rendering','warned','worn','hiding','ghost','avoided','stupid','costly','error','horrible','seat','severe','cuts','odd','loss','frustrating','dreaded','unhappy','hates','hand','two','assembly','sensitive','pressed','pause','bits','particles','push','since','however','pockets','something','waterpik','spray','trying','developed','thus','fix','improved','grip','concerns','quite','mention','instructions','feature','want','range','unfortunately','glad','bathroom','tube','tank','maybe','irrigators','solved','greater','split','tubing','cavities','due','never','finally','family','daughter','bottom','taste','fall','adjustment','eat','ability','lasts','open','reversed','toothache','foods','corrected','puddle','dislike','flosser','losing','excuse','gun','butt','inconvenience','annoyed','depressed','refused','forced','nasty','crazy','charged','sick','charges','frustrated','scared','stubborn','unwanted','exposed','solves','killing','die','ugly','careful','loud','tools','gift','improving','reason','may','turned','simply','pulsing','nozzle','real','kept','mean','apparently','machine','health','actually','expectations','pretty','goes','possible','hold','refill','advertised','wonderful','tip','maximum','root','empties','barely','making','junk','intensity','on/off','minor','loves','newer','find','things','breaking','future','valve','minimal','lead','towards','turning','becomes','position','discovered','going','seem','close','less','delivers','sorts','precise','connect','cleared','deliver','wont','increasing','suggesting','mainly','sprayed','aim','gingivitis','onto','figure','breath','wand','reduced','braun','blast','effectively','gradually','turns','pesky','nuts','noises','competition','attracted','fear','dissatisfied','discarded','defect','challenge','aggressive','intermittent','stunned','becoming','shock','disgusted','dirty','loosing','unsure','embarrassing','harmful','kill','unhealthy','shocked','disturbed','inferior','terribly','badly','irritating','sad','shorter','regrets','suffer','killers','flashlight','mandatory','nervous','torture','disaster','automatically','knocked','malfunctioned','alas','occasions','vibrated','set','fun','sound','occasionally','superior','spend','pulse','returning','im','closed','pieces','stuff','difference','pocket','someone','satisfied','keep','brushed','purchased','release','disease','knew','everyone','tonsils','pushed','throat','meat','description','week','painful','started','ever','reviewers','year'
