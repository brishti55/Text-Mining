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


--select word from wordorientnew
--having count(distinct uniquesentid)<5 group by word;

select count(word) from topprod1ns_df; -- 7927 unique terms

--create table neg_wordlist as
select neg_terms.id, wordorientnew.word, neg_terms.polarity
from wordorientnew join neg_terms on (wordorientnew.uniquesentid=neg_terms.id);

--create table pos_wordlist as
select pos_terms.id, wordorientnew.word, pos_terms.polarity
from wordorientnew join pos_terms on (wordorientnew.uniquesentid=pos_terms.id);

-- Table for P(term) where P(t)=number of sentences in which the term appears(DF)/total number of sentences 
--drop table fp_pt;
--create table fp_pt as 
select distinct word, df, (df/15380) as pt from topprod1ns_df
where df > 2 and length(word)>1;

--Total number of sentences in class with term
select count(distinct id) from pos_wordlist; --12131

--create intermediate table 1 to calculate information gain P(class|term)
create table ig_int_1 as 
select pos_wordlist.id, word, df from pos_wordlist join topprod1ns_df using(word)
order by topprod1ns_df.df desc;

--drop table ig_int_2;
--create table ig_int_2 as
select word, count(distinct id) as total from ig_int_1
group by word
order by total desc;

--Table for calculating P(Class|Term) where P(c|t)=Number of sentences in class with term/ total number of sentences with term
--drop table fp_pct;
--create table fp_pct as 
select ig_int_2.word, total, df, (df/15380) as pt, (ig_int_2.total/topprod1ns_df.df) as pct from ig_int_2 join topprod1ns_df on (topprod1ns_df.word = ig_int_2.word)
--where topprod1ns_df.df > 4 and length(ig_int_2.word)>1
where topprod1ns_df.df > 4 and length(topprod1ns_df.word)>1
order by pct desc;

select count(distinct id) from pos_wordlist; --12131

--drop table ig_int_3;
--create table ig_int_3 as 
select ig_int_2.word, (12131-ig_int_2.total) as total_withoutterm, (15380-topprod1ns_df.df) as total_df_withoutterm
from ig_int_2 join topprod1ns_df on (topprod1ns_df.word = ig_int_2.word)
where topprod1ns_df.df > 4 and length(ig_int_2.word)>1
order by total_df_withoutterm desc;

--Table for calculating P(Class|Not Term) where P(c|nt)=Number of sentences in class without the term/ total number of sentences without the term
--drop table fp_pcnt;
create table fp_pcnt as
select word, (total_withoutterm/total_df_withoutterm) as pcnt from ig_int_3
order by pcnt desc;

select count(distinct word) from fp_pcnt; --2037 when df > 4

--drop table ig_int_4;
--create table ig_int_4 as
select fp_pct.word, ((12131/15380)*(log(10,(12131/15380)))) as part1, 
(fp_pct.pt*fp_pct.pct*(log(10,fp_pct.pct))) as part2, 
(1-fp_pct.pt)*fp_pcnt.pcnt*(log(10,fp_pcnt.pcnt)) as part3 
from fp_pct join fp_pcnt on (fp_pct.word = fp_pcnt.word);

--final ig calculation
--drop table fp_ig;
create table fp_ig as
select word, (((-1)*part1)+part2+part3) as finalig from ig_int_4
order by finalig desc;

select * from fp_ig where rownum <=500;

create table sent_word_polarity as
select sentid, word, sentpolarity.polarity from sentpolarity join wordorientnew on (sentpolarity.sentid=wordorientnew.uniquesentid);

--ig top 100 positive class
create table fp_ig200 as select * from 
  (select distinct sentid, polarity as class, word from sent_word_polarity) 
    pivot 
    (count(word) for word in ('water','button','handle','floss','flossing','flow','high','control','setting','hose','one','dial','get','tip','turn','unit','food','teeth','settings','reservoir','start','reach','remove','gum','use','enough','variable','leaking','bleeding','gums','became','little','wo','adjustable','press','starts','months','place','working','first','time','dont','areas','might','lower','adjust','within','mold','still','even','back','places','heart','gets','read','people','getting','solved','small','using','leakage','higher','tank','motor','always','anything','switch','highest','plastic','caused','unless','serious','spots','push','love','eventually','slightly','cause','increase','temporarily','dropped','attention','later','tips','could','sensitive','bit','either','end','despite','spray','realize','constant','around','cold','bacteria','causing','max','valve','fixed','increased','company','plaque','mouth','like','braun','nozzle','make','pleased','highly','removing','pocket','low','pik','sink','tongue','area','pause','without','puddle','toothache','dripping','vary','reversed','corrected','im','hand','less','waterpik','would','periodontal','kind','pump','putting','holding','properly','root','pressed','split','greater','grip','concerns','release','thing','sometimes','want','leaks','two','sound','body','model','level','recommend','new','point','strong','stream','seemed','tube','especially','find','machine','pretty','best','sufficient','thus','fix','developed','kept','assembly','loud','wisdom','quite','way','irrigators','tubing','instructions','mention','seem','found','crown','improving','connect','increasing','suggesting','deliver','wont','sorts','delivers','cleared','precise','put','old','however','bits','previous','never','unfortunately','range','due'));
    
--igtop500
create table fp_ig500 as select * from 
  (select distinct sentid, polarity as class, word from sent_word_polarity) 
    pivot 
    (count(word) for word in ('water','button','handle','floss','flossing','flow','high','control','setting','hose','one','dial','get','tip','turn','unit','food','teeth','settings','reservoir','start','reach','remove','gum','use','enough','variable','leaking','bleeding','gums','became','little','wo','adjustable','press','starts','months','place','working','first','time','dont','areas','might','lower','adjust','within','mold','still','even','back','places','heart','gets','read','people','getting','solved','small','using','leakage','higher','tank','motor','always','anything','switch','highest','plastic','caused','unless','serious','spots','push','love','eventually','slightly','cause','increase','temporarily','dropped','attention','later','tips','could','sensitive','bit','either','end','despite','spray','realize','constant','around','cold','bacteria','causing','max','valve','fixed','increased','company','plaque','mouth','like','braun','nozzle','make','pleased','highly','removing','pocket','low','pik','sink','tongue','area','pause','without','puddle','toothache','dripping','vary','reversed','corrected','im','hand','less','waterpik','would','periodontal','kind','pump','putting','holding','properly','root','pressed','split','greater','grip','concerns','release','thing','sometimes','want','leaks','two','sound','body','model','level','recommend','new','point','strong','stream','seemed','tube','especially','find','machine','pretty','best','sufficient','thus','fix','developed','kept','assembly','loud','wisdom','quite','way','irrigators','tubing','instructions','mention','seem','found','crown','improving','connect','increasing','suggesting','deliver','wont','sorts','delivers','cleared','precise','put','old','however','bits','previous','never','unfortunately','range','due','located','went','bottom','since','holder','real','taste','closed','combo','minimal','lead','towards','finally','hold','though','maybe','possible','adjustment','eat','ability','someone','bathroom','pulsing','may','careful','effectively','particles','wand','feature','coiled','trying','pockets','fall','levels','mean','cordless','cavities','barely','empties','maximum','straight','eye','battery','keep','something','actually','apparently','drain','making','number','started','open','close','normal','changing','aim','mainly','sprayed','future','breaking','pieces','base','amount','going','reason','wp-100','side','position','discovered','simply','turned','tonsils','pushed','providing','contents','meat','throat','disease','turning','becomes','hands','major','spraying','intensity','on/off','minor','junk','gradually','angle','caught','arm','turns','power','standard','breath','lifted','woman','selection','continuous','corners','squirts','canals','tendency','softer','diligent','grow','lips','crank','design','goes','price','really','cord','mine','sinus','flaw','knob','returning','pulse','regular','another','sure','much','year','saying','changed','occasionally','stuff','blast','reduced','top','head','refill','onto','figure','gingivitis','business','crevices','squirt','originally','wrote','tax','noted','fillings','units','inside','piece','happy','set','things','string','great','reviews','functional','sort','including','easily','concern','overall','knew','tooth','painful','action','reviewers','buying','got','via','besides','lt','connection','bulky','reservior','works','full','brushed','container','fresh','days','away','used','cleaning','left','snap','soft','pull','bridge','take','try','note','information','call','convinced','attached','dislodge','countertop','rate','starting','right','quickly','skip','knows','stiff','afford','tounge','sales','telling','didnt','crack','deeper','aware','affordable','glad','basically','build','speed','week','fill','messy','surgery','adequate','rather','else','wet','perhaps','traditional','mirror','important','think','money','able','seems','every','wow','tight','comfortable','daughter','pumping','batteries','opening','chamber','claim','inflammation','ran','waterjet','slight','leaving','tissue','adjusted','weaker','kinda','consistent','big','fact','portable','pick','brush','biggest','bowl','lingual','term','obsolescence','effects','american','builds','september','thirty','letting','willing','twenty','surfaces','bristles','pregnant','rechargable','seated','altogether','descriptions','potential','released','boyfriend','boot','stone','bite','current','brackets','main','years','pop','tends','braces','seal','coil','bend','somewhat','experienced','happen','short','certainly','scraper','also','improved'));