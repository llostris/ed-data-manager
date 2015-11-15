UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Palma de Mallorca'), ',Majorka')
where name = 'Palma de Mallorca';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Łódź'), ',Łodzi')
where name = 'Łódź';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Kraków'), ',Balice,Balicach,Balic')
where name = 'Kraków';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Warszawa'), ',Modlin,Modlina,Modlinie')
where name = 'Warszawa';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Denpasar'), ',Bali')
where name = 'Denpasar';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Kerkira'), ',Korfu')
where name = 'Kerkira';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Paryż'), ',Paryża,Paryża Beauvais,Beauvais,Paryż Beauvais')
where name = 'Paryż';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Ryga'), ',Rydze,Rygi')
where name = 'Ryga';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Budapeszt'), ',Budapesztu, Budapeszcie')
where name = 'Budapeszt';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Poznań'), ',Poznania,Poznaniu')
where name = 'Poznań';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Genewa'), ',Genewy')
where name = 'Genewa';

UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Londyn'), ',Londyn Luton,Luton')
where name = 'Londyn';

INSERT INTO "DataManager_city"(name, forms, country_id)
VALUES ('Sycylia', 'Sycylia', (SELECT ID FROM "DataManager_country" WHERE NAME = 'Włochy'));

INSERT INTO "DataManager_city"(name, forms, country_id)
VALUES ('Szymany', 'Szymany', (SELECT ID FROM "DataManager_country" WHERE NAME = 'Polska'));
