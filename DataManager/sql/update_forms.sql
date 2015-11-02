UPDATE "DataManager_city"
set forms = concat((SELECT forms from "DataManager_city" where name = 'Palma de Mallorca'), ',Majorka')
where name = 'Palma de Mallorca';

