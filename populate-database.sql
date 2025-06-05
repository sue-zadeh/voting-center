-- Insert values into the User table
INSERT INTO User (Username, FirstName, LastName, Role, Status, Password, Email, Location, Image)
VALUES
('alice_smith', 'Alice', 'Smith', 'admin', 'active', '3f9a05750d8bf6d7ba9d3c2444c2ac30479afc44d814308460eb8816ad1ce03b', 'alice@example.com', 'New York', 'image1.jpg'),
('bob_johnson', 'Bob', 'Johnson', 'voter', 'active', 'password2', 'bob@example.com', 'Los Angeles', 'image2.jpg'),
('charlie_williams', 'Charlie', 'Williams', 'voter', 'inactive', 'password3', 'charlie@example.com', 'Chicago', 'image3.jpg'),
('diana_brown', 'Diana', 'Brown', 'voter', 'active', 'password4', 'diana@example.com', 'Houston', 'image4.jpg'),
('gavinx', 'Gavin', 'Xu', 'voter', 'active', 'c40b534b7177581375d7c3fd172e6b69a8583842b871e7876d472ba86fc1e4b5', 'gavinx@voter.com', 'Auckland', 'image4.jpg'),
('gavinx1', 'Gavin', 'Xu', 'admin', 'active', 'c40b534b7177581375d7c3fd172e6b69a8583842b871e7876d472ba86fc1e4b5', 'gavinx@admin.com', 'Auckland', 'gavinadmin.jpg'),
('eve_jones', 'Eve', 'Jones', 'scrutineer', 'active', 'password5', 'eve@example.com', 'Phoenix', 'image5.jpg');

-- Insert values into the Announcement table
INSERT INTO Announcement (CreatedBy, CreatedAt, StartDate, FinishDate, Content)
VALUES
(1, NOW(), '2024-01-01', '2024-12-31', 'Welcome to the Best Walkway 2024 competition! Cast your votes now!'),
(1, NOW(), '2024-02-01', '2024-11-30', 'The Top Coastal Walkway competition is now open for voting!');


-- Insert values into the Competition table
INSERT INTO Competition (Name, Description, StartDate, FinishDate, CreatedBy, ApprovedBy, Status)
VALUES
('Best Walkway 2024', 'Vote for the best walkway in New Zealand for 2024.', '2024-01-01', '2024-12-31', 1, 1, 'active'),
('Competition 2', 'A competition to find the best coastal walkway.', '2024-02-01', '2024-11-30', 2, 1, 'active');



-- Insert values into the Competitor table
INSERT INTO Competitor (Name, Image, Description, CreatedBy)
VALUES
('Milford Track', 'milford.jpg', 'This walkway is located in Fiordland National Park in Te Anau. The Milford Track is a world-famous hike through Fiordland National Park, offering stunning views of mountains, valleys, and waterfalls. Excellent facilities for camping.', 1),
('Routeburn Track', 'routeburn.jpg', 'This walkway connects Fiordland and Mount Aspiring National Parks, located in Queenstown. The Routeburn Track features high mountain passes, crystal-clear rivers, and impressive valleys. Great camping spots and huts along the way.', 2),
('Tongariro Alpine Crossing', 'tongariro.jpg', 'This walkway is located in Tongariro National Park in the Central North Island. The Tongariro Alpine Crossing offers an otherworldly experience, with volcanic landscapes, emerald lakes, and panoramic views. Popular for day hikes with well-maintained camping facilities.', 3),
('Abel Tasman Coast Track', 'abeltasman.jpg', 'This walkway is located in Abel Tasman National Park in Nelson. The Abel Tasman Coast Track explores golden beaches, lush native forests, and clear coastal waters. Various campsites and comfortable huts are available.', 4),
('Heaphy Track', 'heaphy.jpg', 'This walkway is located in Kahurangi National Park in Golden Bay. The Heaphy Track traverses diverse landscapes, from lush forests to rugged coastline. Renowned for its remote beauty and excellent camping facilities.', 5),
('Kepler Track', 'kepler.jpg', 'This walkway is located in Fiordland National Park in Te Anau. The Kepler Track is a circular route showcasing beautiful beech forests, alpine tops, and glacial valleys. Excellent huts and campsites along the way.', 1),
('Rakiura Track', 'rakiura.jpg', 'This walkway is located on Stewart Island near Oban. The Rakiura Track offers a remote wilderness experience, with lush rainforest, sandy beaches, and abundant birdlife. Well-maintained huts and campsites.', 2),
('Lake Waikaremoana Track', 'lake_waikaremoana.jpg', 'This walkway is located in Te Urewera in the Hawke\'s Bay region. The Lake Waikaremoana Track takes you around Lake Waikaremoana, offering stunning views, lush forests, and a tranquil atmosphere. Great for multi-day hikes with camping options.', 3),
('Whanganui Journey', 'whanganui.jpg', 'This walkway is located on the Whanganui River in Whanganui. The Whanganui Journey is unique among New Zealand\'s Great Walks, this journey is a river adventure, perfect for canoeing through deep gorges and lush forest. Campsites and huts available.', 4),
('Paparoa Track', 'paparoa.jpg', 'This walkway is located in Paparoa National Park in the West Coast region. The Paparoa Track offers breathtaking views, deep canyons, and lush forests. It\'s New Zealand\'s newest Great Walk, with well-maintained huts and campsites.', 5),
('Queen Charlotte Track', 'queen_charlotte.jpg', 'This walkway is located in the Marlborough Sounds near Picton. The Queen Charlotte Track combines beautiful coastal views, lush forests, and historical sites. A variety of accommodation options are available.', 1),
('Pinnacles Track', 'pinnacles.jpg', 'This walkway is located in the Coromandel Peninsula near Thames. The Pinnacles Track is a popular hike offering panoramic views from the Pinnacles. Excellent facilities for camping.', 2),
('Pouakai Crossing', 'pouakai.jpg', 'This walkway is located in Egmont National Park near New Plymouth. The Pouakai Crossing offers stunning views of Mount Taranaki, alpine wetlands, and lush forest. Great for day hikes with camping options.', 3),
('Mount Taranaki Summit Track', 'mount_taranaki.jpg', 'This walkway is located in Egmont National Park near New Plymouth. The Mount Taranaki Summit Track is a challenging climb to the summit of Mount Taranaki, offering panoramic views. Limited facilities, so preparation is essential.', 4),
-- ('Hump Ridge Track', 'hump_ridge.jpg', 'This walkway is located in Fiordland National Park in Tuatapere. The Hump Ridge Track offers spectacular views of rugged coastlines, mountains, and forests. Unique accommodation options available.', 5),
-- ('Cape Reinga Coastal Walkway', 'cape_reinga.jpg', 'This walkway is located at the northernmost tip of New Zealand near Cape Reinga. The Cape Reinga Coastal Walkway offers stunning coastal views and rich Maori history.', 1),
-- ('Te Araroa Trail', 'te_araroa.jpg', 'This trail spans the length of New Zealand. The Te Araroa Trail is New Zealand\'s longest trail, a true adventure for those looking to experience all of New Zealand\'s landscapes.', 2),
-- ('Mount Cook National Park Walks', 'mount_cook.jpg', 'This walkway is located in Aoraki/Mount Cook National Park in the Canterbury region. The Mount Cook National Park Walks offer views of New Zealand\'s highest peak, glaciers, and alpine scenery. Great camping facilities and huts.', 3),
-- ('Arthur’s Pass Walking Tracks', 'arthurs_pass.jpg', 'This walkway is located in Arthur\'s Pass National Park in the Canterbury region. The Arthur’s Pass Walking Tracks offer a variety of walks through alpine landscapes, lush forests, and dramatic gorges. Basic huts and campsites available.', 4),
-- ('Rob Roy Glacier Track', 'rob_roy.jpg', 'This walkway is located in Mount Aspiring National Park near Wanaka. The Rob Roy Glacier Track is a beautiful day hike offering stunning views of the Rob Roy Glacier. Well-maintained track with basic facilities.', 5),
-- ('Mount Aspiring Hut Walk', 'mount_aspiring.jpg', 'This walkway is located in Mount Aspiring National Park near Wanaka. The Mount Aspiring Hut Walk is a gentle walk to Mount Aspiring Hut, offering stunning alpine scenery and river views. Great for families and beginner hikers.', 1),
-- ('Hooker Valley Track', 'hooker_valley.jpg', 'This walkway is located in Aoraki/Mount Cook National Park in the Canterbury region. The Hooker Valley Track is a popular walk offering stunning views of glaciers, mountains, and alpine lakes. Accessible to all ages.', 2),
-- ('Ben Lomond Track', 'ben_lomond.jpg', 'This walkway is located in Queenstown. The Ben Lomond Track is a challenging climb with rewarding panoramic views of Queenstown and the surrounding mountains. No facilities on the track.', 3),
-- ('Mount Kaukau Walk', 'mount_kaukau.jpg', 'This walkway is located in Wellington. The Mount Kaukau Walk is a popular walk offering panoramic views of the city, harbor, and beyond.', 4),
-- ('Waiheke Island Coastal Walk', 'waiheke.jpg', 'This walkway is located on Waiheke Island near Auckland. The Waiheke Island Coastal Walk explores the beautiful coastline, with stunning views, vineyards, and beaches. Plenty of accommodation options.', 5),
-- ('Catlins Coastal Heritage Trail', 'catlins.jpg', 'This walkway is located in The Catlins near Balclutha. The Catlins Coastal Heritage Trail offers the remote and rugged coastline, with waterfalls, wildlife, and stunning coastal views.', 1),
-- ('Rangitoto Summit Track', 'rangitoto.jpg', 'This walkway is located on Rangitoto Island near Auckland. The Rangitoto Summit Track offers a walk to the summit of Auckland\'s iconic volcanic island, offering panoramic views of the city and the Hauraki Gulf.', 2),
-- ('Blue Pools Walk', 'blue_pools.jpg', 'This walkway is located in Haast Pass near Wanaka. The Blue Pools Walk offers a short walk to crystal-clear pools in the middle of the forest, offering a peaceful and picturesque setting.', 3),
-- ('Roy\'s Peak Track', 'roys_peak.jpg', 'This walkway is located in Wanaka. The Roy\'s Peak Track is a challenging hike with stunning views over Lake Wanaka and the Southern Alps. No facilities on the track.', 4),
-- ('Cape Brett Track', 'cape_brett.jpg', 'This walkway is located in the Bay of Islands near Russell. The Cape Brett Track offers a coastal walk with stunning views of the Bay of Islands, with options for overnight stays in remote locations.', 5),
-- ('Crater Rim Walkway', 'crater_rim.jpg', 'This walkway is located in Banks Peninsula near Christchurch. The Crater Rim Walkway explores the volcanic landscape of Banks Peninsula, with stunning views of the harbor and the surrounding area.', 1),
-- ('Abel Tasman National Park Day Walks', 'abel_tasman_day.jpg', 'This walkway is located in Abel Tasman National Park in Nelson. The Abel Tasman National Park Day Walks offer a variety of day walks, offering stunning coastal views.', 2),
-- ('Lake Matheson Walk', 'lake_matheson.jpg', 'This walkway is located in Westland National Park near Fox Glacier. The Lake Matheson Walk offers a short walk around the picturesque Lake Matheson, famous for its mirror-like reflections of Mount Cook and Mount Tasman.', 3),
-- ('Fiordland National Park Walks', 'fiordland.jpg', 'This walkway is located in Fiordland National Park in Te Anau. The Fiordland National Park Walks offer a variety of walks through remote and rugged beauty, from short strolls to multi-day hikes.', 4),
-- ('Moeraki Boulders Walk', 'moeraki.jpg', 'This walkway is located in Moeraki near Oamaru. The Moeraki Boulders Walk offers a short walk to see the famous spherical boulders on Koekohe Beach. A unique geological feature of New Zealand.', 5),
-- ('Otago Central Rail Trail', 'otago_rail.jpg', 'This walkway is located in Central Otago near Clyde. The Otago Central Rail Trail is a popular cycling and walking trail through the heart of Central Otago, offering stunning landscapes and rich history.', 1),
-- ('Waiau Pass Track', 'waiau_pass.jpg', 'This walkway is located in Nelson Lakes National Park in Saint Arnaud. The Waiau Pass Track is a challenging alpine track offering stunning views and remote wilderness.', 2),
-- ('Aoraki Mount Cook Village Short Walks', 'aoraki_village.jpg', 'This walkway is located in Aoraki/Mount Cook National Park in the Canterbury region. The Aoraki Mount Cook Village Short Walks offer a variety of short walks with stunning alpine scenery around Mount Cook Village.', 3),
-- ('Doubtful Sound Walks', 'doubtful_sound.jpg', 'This walkway is located in Fiordland National Park in Manapouri. The Doubtful Sound Walks offer a variety of walks through remote beauty with stunning views and tranquility.', 4),
-- ('Mount Holdsworth Track', 'mount_holdsworth.jpg', 'This walkway is located in the Tararua Range near Masterton. The Mount Holdsworth Track offers a popular walk with stunning views and a range of accommodation options.', 5),
-- ('Rangitoto Island Walks', 'rangitoto_walks.jpg', 'This walkway is located on Rangitoto Island near Auckland. The Rangitoto Island Walks explore the volcanic landscape and historic sites of Rangitoto Island with a variety of walks.', 1),
-- ('Craters of the Moon Track', 'craters_of_the_moon.jpg', 'This walkway is located in Taupo. The Craters of the Moon Track offers a short walk through a geothermal area near Taupo, offering bubbling mud pools and steaming vents.', 2),
-- ('Te Whara Track', 'te_whara.jpg', 'This walkway is located in Northland near Whangarei. The Te Whara Track is a challenging coastal walk offering stunning views and rich Maori history.', 3),
-- ('Kauaeranga Kauri Trail', 'kauaeranga_kauri.jpg', 'This walkway is located in Coromandel Forest Park near Thames. The Kauaeranga Kauri Trail offers a scenic walk through the Coromandel Forest Park, with views of ancient Kauri trees and lush forest.', 4),
-- ('Goldie Bush Walkway', 'goldie_bush.jpg', 'This walkway is located in the Waitakere Ranges near Auckland. The Goldie Bush Walkway offers a walk through native forest and along a stream, offering a peaceful retreat.', 5),
-- ('Gillespie Pass Circuit', 'gillespie_pass.jpg', 'This walkway is located in Mount Aspiring National Park near Wanaka. The Gillespie Pass Circuit is a challenging alpine circuit offering stunning views and remote wilderness.', 1),
-- ('Hollyford Track', 'hollyford.jpg', 'This walkway is located in Fiordland National Park near Milford Sound. The Hollyford Track offers a remote and stunning walk through Fiordland, with breathtaking views of mountains, rivers, and forests.', 2),
-- ('Queenstown Hill Time Walk', 'queenstown_hill.jpg', 'This walkway is located in Queenstown. The Queenstown Hill Time Walk offers a short but steep walk with panoramic views of Queenstown and Lake Wakatipu.', 3),
-- ('Karangahake Gorge Historic Walkway', 'karangahake.jpg', 'This walkway is located in Karangahake Gorge near Paeroa. The Karangahake Gorge Historic Walkway offers a walk through a historic gold mining area, with stunning scenery and rich history.', 4);

INSERT INTO CompetitionCompetitor (CompetitionID, CompetitorID)
VALUES
(1, 1), -- Milford Track in Best Walkway 2024
(1, 2), -- Abel Tasman Coast Track in Best Walkway 2024
(2, 2), -- Abel Tasman Coast Track in Top Coastal Walkway
(2, 3); -- Routeburn Track in Top Coastal Walkway


-- Insert values into the Vote table
INSERT INTO Vote (IPAddress, CompetitionID, CompetitorID, Status, VotedBy, VotedAt)
VALUES
('192.168.1.1', 1, 1, 'active', 2, NOW()), -- Jane votes for Milford Track in Best Walkway 2024
('192.168.1.2', 1, 2, 'active', 3, NOW()), -- Emily votes for Abel Tasman Coast Track in Best Walkway 2024
('192.168.1.3', 2, 3, 'active', 2, NOW()); -- Jane votes for Routeburn Track in Top Coastal Walkway


-- UPDATE Competition 
-- SET Name = 'Competition 2', 
--     Description = 'A competition to find the best coastal walkway.' 
-- WHERE CompetitionID = 2;
