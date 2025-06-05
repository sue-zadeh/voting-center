import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from mysql.connector import connect, Error
from datetime import datetime
from app import app
import app.connect as connect

app.secret_key = 'e2e62cdb171271f0b12e5043f9f84208eba1f05c8658704e'
PASSWORD_SALT = '1234abcd'
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

hashing = Hashing(app)

db_connection = None

def getCursor(dictionary=False, buffered=False):
    global db_connection

    try:
        if db_connection is None or not db_connection.is_connected():
            db_connection = mysql.connector.connect(
                user=connect.dbuser,
                password=connect.dbpass,
                host=connect.dbhost,
                database=connect.dbname,
                auth_plugin='mysql_native_password',
                autocommit=True
            )
            print("Connection successful")

        cursor = db_connection.cursor(dictionary=dictionary, buffered=buffered)
        return cursor, db_connection

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        return None, None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}
#------competitors---#
@app.route('/competitors')
def competitors():
    cursor, conn = getCursor(dictionary=True)
    cursor.execute("SELECT * FROM Competitor")
    competitors = cursor.fetchall()
    
    image_urls = {
    "milford.jpg": "https://www.realnz.com/media/697716/milford-track-min.jpg",
    "routeburn.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Tarn_at_Key_Summit%2C_a_side_track_on_the_Routeburn_Track.jpg/1280px-Tarn_at_Key_Summit%2C_a_side_track_on_the_Routeburn_Track.jpg",
    "tongariro.jpg": "https://the-park.co.nz/wp-content/uploads/2019/01/Emerald-Lake-Tongariro.jpeg",
    "abeltasman.jpg": "https://www.atlasandboots.com/wp-content/uploads/2018/08/Hiking-the-Abel-Tasman-Coast-Track-1.jpg",
    "heaphy.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/HeaphyRiver.jpg/1280px-HeaphyRiver.jpg",
    "kepler.jpg": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0d/c4/ef/34/kepler-track-is-one-of.jpg?w=1200&h=-1&s=1",
    "rakiura.jpg": "https://wilderness-production.imgix.net/2020/08/Rakiura-Track-Southland-New-Zealand-Credit-Great-South-3.jpg?auto=compress%2Cformat&fit=scale&h=1292&ixlib=php-3.3.1&w=1980&wpsize=full_width",
    "lake_waikaremoana.jpg": "https://media-cdn.tripadvisor.com/media/photo-s/05/5f/8a/de/lake-waikaremoana.jpg", 
    "whanganui.jpg": "https://destinationlesstravel.com/wp-content/uploads/2019/02/DSC_5120-768x513.jpg.webp",
    "paparoa.jpg": "http://tramper.nz/files/objectversions/13136/IMG_1222%20(Large).jpg",
    "queen_charlotte.jpg": "https://images.nzgeo.com/2015/08/Page-164-1300x867.jpg",
    "pinnacles.jpg":  "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/05/65/7e/9f/putangirua-pinnacles.jpg?w=1200&h=-1&s=1", 
    # "pouakai.jpg": "https://dbijapkm3o6fj.cloudfront.net/resources/14479,1004,1,6,4,0,600,450/-4051-/20210506163119/pouakai-crossing-mount-taranaki.jpeg",
    # "mount_taranaki.jpg": "https://www.pinyourfootsteps.com/wp-content/uploads/2019/12/NZNI-117-1024x768.jpg",
    # "hump_ridge.jpg": "https://youngadventuress.com/wp-content/uploads/2018/02/0O6A6968-copy-1920x1280.jpg", 
    # "cape_reinga.jpg": "https://www.kiwishirts.com/wp-content/uploads/2021/05/Cape-Reinga-Walkway-to-Lighthouse.jpg",
    # "te_araroa.jpg": "https://1964.co.nz/wp-content/uploads/2022/07/1-slide-new-zealand-lake-pukaki-and-mount-cook-pano-1284x700.jpeg",
    # "mount_cook.jpg": "https://media-cdn.tripadvisor.com/media/attractions-splice-spp-674x446/06/6f/72/53.jpg",
    # "arthurs_pass.jpg": "https://hikingscenery.com/wp-content/uploads/2021/07/1110382-1024x683.jpg",
    # "rob_roy.jpg": "https://hikingscenery.com/wp-content/uploads/2019/12/DSCN4953-1024x768.jpg",
    # "mount_aspiring.jpg": "https://youngadventuress.com/wp-content/uploads/2020/01/DSC01113-1920x1280.jpg", 
    # "hooker_valley.jpg": "https://hikingscenery.com/wp-content/uploads/2019/05/IMG_20151222_134407-1024x576.jpg",
    # "ben_lomond.jpg": "https://newzealandwanderer.com/wp-content/uploads/Ben-Lomond-track-Queenstown-2.jpg",
    # "mount_kaukau.jpg": "https://images.wildthings.club/20201215_123721.jpg?tr=w-960,h-575",
    # "waiheke.jpg": "https://cdn-boial.nitrocdn.com/lrJSTMUhHaOSnJLNCZvsPgAAIjWcEmgs/assets/images/optimized/rev-5d8b81f/nzpocketguide.com/wp-content/uploads/2019/10/walks-in-waiheke-island.jpg",
    # "catlins.jpg":   "https://www.newzealand.com/assets/Tourism-NZ/Southland/img-1536992911-3686-27616-p-002C3225-F8FF-6526-D9C2C67BF117FDA0-2544003__aWxvdmVrZWxseQo_CropResizeWzY1MCw0ODgsODAsImpwZyJd.JPG",
    # "rangitoto.jpg": "https://twoatsea.com/wp-content/uploads/2020/07/Rangitoto-Hike-1.jpg",
    # "blue_pools.jpg": "https://www.loveyaguts.co.nz/wp-content/uploads/2021/05/Blue_Pools_Wanaka-1.jpg",
    # "roys_peak.jpg": "https://theworldtravelguy.com/wp-content/uploads/2020/04/DSCF0882-2.jpg",
    # "cape_brett.jpg": "https://www.newzealand.com/assets/Tourism-NZ/Northland-Bay-of-Islands/img-1536920979-1791-26953-7308845A-0537-5AF8-4C475E1BDEF4AC8C__aWxvdmVrZWxseQo_FocalPointCropWzcwMCwxOTIwLDY0LDYwLDc1LCJqcGciLDY1LDIuNV0.jpg",
    # "crater_rim.jpg": "https://img.rezdy.com/PRODUCT_IMAGE/144021/IMG_1561_lg.jpg",
    # "abel_tasman_day.jpg": "https://www.nztravelorganiser.com/wp-content/uploads/2019/09/abel-tasman.jpg",
    # "lake_matheson.jpg": "https://www.lakematheson.com/wp-content/uploads/2022/07/Photo-10-05-22-11-40-47-AM.jpg",
    # "fiordland.jpg": "https://www.zicasso.com/static/53799d21612e2bf32ab9554b7230e6f2/e5112/53799d21612e2bf32ab9554b7230e6f2.webp",
    # "moeraki.jpg": "https://img.atlasobscura.com/vVrMhkt5JW9Bg0CaKPZdo3rE--e5H7Oc-6afPYimmNE/rt:fit/w:1200/q:81/sm:1/scp:1/ar:1/aHR0cHM6Ly9hdGxh/cy1kZXYuczMuYW1h/em9uYXdzLmNvbS91/cGxvYWRzL3BsYWNl/X2ltYWdlcy9mMTBj/ZWQ2Mi0zZjIzLTQy/ZDYtODRjZC1hMjcy/NTg1OGMzMjVkMDhi/MTA2YzNiODFjMTUx/NWFfRFNDXzE3MjEu/anBn.jpg",
    # "otago_rail.jpg": "#",
    # "waiau_pass.jpg": "#",
    # "aoraki_village.jpg": "#",
    # "doubtful_sound.jpg": "#",
    # "mount_holdsworth.jpg": "#",
    # "rangitoto_walks.jpg": "#",
    # "craters_of_the_moon.jpg": "#",
    # "te_whara.jpg": "#",
    # "kauaeranga_kauri.jpg": "#",
    # "goldie_bush.jpg": "#",
    # "gillespie_pass.jpg": "#",
    # "hollyford.jpg": "#",
    # "queenstown_hill.jpg": "#",
    # "karangahake.jpg": "#",
    # "otago_rail_2.jpg": "#"
}

#---------- images for the modal----#
    image_details = {
        "milford.jpg": [
            "https://i.redd.it/0r2ylhsvx3b21.jpg",
            "https://milfordtrack.net/wp-content/uploads/2019/06/Milford-Sound.jpg"
        ],
        "routeburn.jpg": [
          "https://upload.wikimedia.org/wikipedia/commons/c/c6/Forge_Flat.jpg",
          "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0a/57/3f/55/photo1jpg.jpg?w=1200&h=-1&s=1"
        ],
       "tongariro.jpg": [
        "https://theplanetd.com/images/Tongariro-Alpine-Crossing-Emerald-Lakes.jpg",
        "https://cdn.getyourguide.com/img/tour/166663853c9465d35278213b4310953dc024f472b8379384ff78c2298d108348.jpeg/145.jpg" 
       ],
      "abeltasman.jpg": [
        "https://teara.govt.nz/files/29096-pc.jpg",
        "https://tramposaurus.com/wp-content/uploads/2021/07/Abel-Tasman-Coast-Track-New-Zealand-Split-Apple-Rock-1024x576.jpg"
      ],
      "heaphy.jpg": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Brown_Hut_10.jpg/1280px-Brown_Hut_10.jpg",
      "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/HigherPointHeaphy.jpg/1280px-HigherPointHeaphy.jpg"
      ],
   
      "kepler.jpg": [
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0d/c4/ef/37/kepler-track-is-one-of.jpg?w=1200&h=-1&s=1",
        "https://plutoniclove.com/wp-content/uploads/2019/03/39223328504_a7dc3c9054_o.jpg?w=1280"
      ],
  "rakiura.jpg": [
         "https://www.traxplorio.com/wp-content/uploads/2021/02/d4ce1878-1e4c-4ceb-adf9-799cd16a8efb-scaled.jpeg",
        "https://www.traxplorio.com/wp-content/uploads/2021/02/f4abacfb-f8a7-43ee-8984-8e9f1161aacb.jpeg"
     ],
  "lake_waikaremoana.jpg": [
       "https://media-cdn.tripadvisor.com/media/photo-s/05/c6/ba/11/lake-waikaremoana.jpg",
       "https://media-cdn.tripadvisor.com/media/photo-s/05/5f/8a/dc/lake-waikaremoana.jpg"
  ],
  "whanganui.jpg": [
    "https://destinationlesstravel.com/wp-content/uploads/2019/02/DSC_5159-768x513.jpg.webp",
    "https://destinationlesstravel.com/wp-content/uploads/2019/02/DSC_5191-768x513.jpg.webp"
  ],
  "paparoa.jpg": [
    "https://ramblings.nz/wp-content/uploads/2021/04/paparoa_featured2.jpg", 
    "https://ramblings.nz/wp-content/uploads/2021/04/paparoa_gorge_800w.jpg"
   ],
    "queen_charlotte.jpg": [
      "https://img.rezdy.com/PRODUCT_IMAGE/30362/b3a3df4037124b24878be2803ed7378cClose_up_SC_lg.jpg",
      "https://img.rezdy.com/PRODUCT_IMAGE/30362/6.jpg"
   ],  
  "pinnacles.jpg": [
      "https://i0.wp.com/www.jennyfaraway.com/wp-content/uploads/2019/03/DSC_0326-1.jpg?w=1024&ssl=1",
      "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/05/65/7e/b2/putangirua-pinnacles.jpg?w=1200&h=-1&s=1"
   ]
#   "pouakai.jpg": [
#      "https://wtmc.org.nz/wp-content/uploads/2021/06/IMG20210522123443-scaled.jpg",
#      "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/17/64/d7/70/img-20190423-182906-310.jpg?w=1200&h=-1&s=1"
#   ],
#  "mount_taranaki.jpg": [
#    "https://www.pinyourfootsteps.com/wp-content/uploads/2019/12/NZNI-115-1024x768.jpg",
#    "https://lastminutewanders.com/wp-content/uploads/2019/06/rsz_img_2989.jpg"
#    ],
#  "hump_ridge.jpg": [
#   "https://youngadventuress.com/wp-content/uploads/2018/01/0O6A6084-copy-1920x1280.jpg",
#   "https://youngadventuress.com/wp-content/uploads/2018/01/0O6A6774-copy-1920x1280.jpg"
#    ],
#  "cape_reinga.jpg": [
#   "https://www.kiwishirts.com/wp-content/uploads/2021/05/Cape-Reinga-Underworld-1.jpg",
#   "https://www.kiwishirts.com/wp-content/uploads/2021/05/Cape-Reinga-Ocean-1.jpg"
#   ],
#  "te_araroa.jpg": [
#    "https://1964.co.nz/wp-content/uploads/2022/07/IMG_5551-1900x1267.jpeg",
#    "https://1964.co.nz/wp-content/uploads/2022/07/1639080483005-710x399.jpeg"
#    ],
#  "mount_cook.jpg": [
#    "https://www.kiwishirts.com/wp-content/uploads/2021/04/Routeburn-Track-Swingbridge-1.jpg",
#    "https://www.kiwishirts.com/wp-content/uploads/2021/04/Routeburn-Track-View-1.jpg"
#    ],
#  "arthurs_pass.jpg": [
#      "https://hikingscenery.com/wp-content/uploads/2020/10/1070551-1024x448.jpg",
#      "https://hikingscenery.com/wp-content/uploads/2020/11/PXL_20201112_194344292-768x1024.jpg"
#    ],
#  "rob_roy.jpg": [
#    "https://api.lakewanaka.co.nz/assets/Uploads/Wanaka-Roby-Roy-Track-OfTwoLands2__FocusFillWzE5MjAsMTA4MCxmYWxzZSwwXQ.jpg",
#    "https://api.lakewanaka.co.nz/assets/Uploads/Wanaka-Roby-Roy-Track-OfTwoLands4__FocusFillWzE5MjAsMTA4MCxmYWxzZSwwXQ.jpg"
#   ],
#   "mount_aspiring.jpg": [
#     "https://hikingscenery.com/wp-content/uploads/2023/01/1140374-840x450.jpg",
#     "https://youngadventuress.com/wp-content/uploads/2020/01/DSC02075-1920x1280.jpg"
#     ],
#  "hooker_valley.jpg": [
#      "https://digitaltravelcouple.com/wp-content/uploads/2023/02/hooker-valley-track-mount-cook.webp",
#      "https://i0.wp.com/moderatelyadventurous.com/wp-content/uploads/2022/06/IMG_9781-2.jpg?resize=1200%2C550&ssl=1"
#    ],
#  "ben_lomond.jpg": [
#    "https://newzealandwanderer.com/wp-content/uploads/Ben-Lomond-Track-Queenstown.jpg",
#    "https://newzealandwanderer.com/wp-content/uploads/Hiking-Ben-Lomond-Queenstown-1.jpg"
#    ],
#   "mount_kaukau.jpg": [
#     "https://cdn-boial.nitrocdn.com/lrJSTMUhHaOSnJLNCZvsPgAAIjWcEmgs/assets/images/optimized/rev-5d8b81f/nzpocketguide.com/wp-content/uploads/2019/10/Waiheke-Island-Forest-Walk_optimized.jpg",
#     "https://cdn-boial.nitrocdn.com/lrJSTMUhHaOSnJLNCZvsPgAAIjWcEmgs/assets/images/optimized/rev-5d8b81f/nzpocketguide.com/wp-content/uploads/2019/10/walks-of-waiheke-island.jpg"
#     ],
#   "waiheke.jpg": [
#     "https://www.newzealand.com/assets/Tourism-NZ/Southland/img-1536992923-2260-27616-5341246067_8787346bcd_o__aWxvdmVrZWxseQo_CropResizeWzUwMCwzNzUsODAsImpwZyJd.jpg",
#     "https://www.catlins.org.nz/assets/bulkUpload/Nugget-Point-Southland-New-Zealand-Credit-Sam-Deuchrass-2__FocusFillWzQzMiw0NTAsIngiLDEyMV0.jpg"
#     ],
#  "catlins.jpg": [
#    "https://www.hickerphoto.com/images/600/mclean-waterfall-catlins-53713.jpg",
#    "https://www.newzealand.com/assets/Tourism-NZ/Southland/img-1536992923-2260-27616-5341246067_8787346bcd_o__aWxvdmVrZWxseQo_CropResizeWzY1MCw0ODgsODAsImpwZyJd.jpg"
#    ], 
#  "rangitoto.jpg": [
#    "https://twoatsea.com/wp-content/uploads/2020/07/Rangitoto-Hike-2.jpg",
#    "https://twoatsea.com/wp-content/uploads/2020/07/Rangitoto-Hike-4.jpg"
#    ],
#   "blue_pools.jpg": [
#     "https://wanakabiketours.co.nz/wp-content/uploads/2022/06/IMG_20200719_154315-edited-768x433.jpg",
#      "https://seethesouthisland.com/wp-content/uploads/2017/11/blue-pools-car-park-view-nz.jpg"
#     ],
#   "roys_peak.jpg": [
#     "https://theworldtravelguy.com/wp-content/uploads/2020/04/DSCF0724.jpg",
#     "https://theworldtravelguy.com/wp-content/uploads/2020/04/DSCF0735.jpg"
#     ],
#    "cape_brett.jpg": [
#      "https://www.newzealand.com/assets/Tourism-NZ/Northland-Bay-of-Islands/img-1536992556-3897-18551-p-0D175DF7-9609-CD0C-44F554CD9371A781-2544003__aWxvdmVrZWxseQo_CropResizeWzEyMDAsbnVsbCw3NSwianBnIl0.jpg",
#      "https://media-cdn.tripadvisor.com/media/photo-s/1c/69/59/ee/cape-brett.jpg"
#      ],
#  "crater_rim.jpg": [
#    "https://admin.planmywalk.nz/assets/UserReviewImages/8c6a52874ee13bb67aa08fc756aec6ddae5bb149__FocusFillWyIwLjAwIiwiMC4wMCIsMTkyMCw2MDBd.webp",
#    "https://img.rezdy.com/PRODUCT_IMAGE/144021/Crater_Rim_Walks_2.JPG"
#    ],
#  "abel_tasman_day.jpg": [
#    "https://www.nztravelorganiser.com/wp-content/uploads/2019/09/wilsons-abel-tasman.jpg",
#    "https://www.nztravelorganiser.com/wp-content/uploads/2019/09/abel-tasman-national-park.jpg"
#    ],
#  "lake_matheson.jpg": [
#    "https://www.lakematheson.com/wp-content/uploads/2022/06/16-1.jpg",
#    "https://www.lakematheson.com/wp-content/uploads/2022/06/4.jpg"
#    ],
#  "fiordland.jpg": [
#    "https://www.tripsavvy.com/thmb/lrq9vG05E9WVs7ndm4xcID4VMYw=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/coverimage-12a85e88fd60486d88557d77451a1a24.jpg",
#   "https://www.tripsavvy.com/thmb/TFjFlrNIztYtod2oyZlHxEwsWg0=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/naturewalk-813c738aff07486f8786bc249968939e.jpg"
#    ],
#  "moeraki.jpg": [
#    "https://img.atlasobscura.com/01Gg-Abqx5iDEPHeZXhzXXo3NV3l1uzmY0M1iofp2Go/rt:fit/w:1200/q:81/sm:1/scp:1/ar:1/aHR0cHM6Ly9hdGxh/cy1kZXYuczMuYW1h/em9uYXdzLmNvbS91/cGxvYWRzL3BsYWNl/X2ltYWdlcy84NjY2/MTliYWY1YjUyZmNl/YWRhNTdlMDJlNTg4/MzBhZGM4MmRhMTNk/LmpwZw.jpg",
#    "https://img.atlasobscura.com/wyUy6It62--Ju2MH2qmDSTAL2orz_aT0Lz1kSPDsnZY/rt:fit/w:1200/q:81/sm:1/scp:1/ar:1/aHR0cHM6Ly9hdGxh/cy1kZXYuczMuYW1h/em9uYXdzLmNvbS91/cGxvYWRzL3BsYWNl/X2ltYWdlcy81YzMw/MTY2MGU0YjIxMWNi/MzlkNTUyM2I4Mzlk/ZjhkM2YzYmJmYTY0/LmpwZw.jpg"
#    ],
# "otago_rail.jpg": [],
# "waiau_pass.jpg": [],
# "aoraki_village.jpg": [],
# "doubtful_sound.jpg": [],
# "mount_holdsworth.jpg": [],
# "rangitoto_walks.jpg": [],
# "craters_of_the_moon.jpg": [],
# "te_whara.jpg": [],
# "kauaeranga_kauri.jpg": [],
# "goldie_bush.jpg": [],
# "gillespie_pass.jpg": [],
# "hollyford.jpg": [],
# "queenstown_hill.jpg": [],
# "karangahake.jpg": [
#                     ],
# "otago_rail_2.jpg": [
  
# ]
    }
       
   # Pass both the names and descriptions to the template
   # Assign URLs and other data to competitors
    for competitor in competitors:
        image_key = competitor['Image']
        competitor['image_url'] = image_urls.get(image_key, "")
        competitor['image_detail_1'] = image_details.get(image_key, [""])[0]
        competitor['image_detail_2'] = image_details.get(image_key, ["", ""])[1]

    cursor.close()
    conn.close()
    return render_template('competitors.html', competitors=competitors)

#-------voting center-----------------#
@app.route('/voting', methods=['GET', 'POST'])
def voting():
    if 'UserID' not in session:
        flash('Please log in to view the Voting Center.', 'info')
        return redirect(url_for('login'))

    cursor, conn = getCursor(dictionary=True)
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('login'))

    # Fetch active competitions
    cursor.execute("SELECT * FROM Competition WHERE Status = 'active'")
    competitions = cursor.fetchall()

    if request.method == 'POST':
        competition_id = request.form['competition']
        competitor_id = request.form['competitor']

        # Check if the user has already voted in this competition
        cursor.execute("SELECT * FROM Vote WHERE VotedBy = %s AND CompetitionID = %s", (session['UserID'], competition_id))
        vote = cursor.fetchone()

        if vote:
            flash('You have already voted in this competition.', 'warning')
            return redirect(url_for('voting'))
        else:
            try:
                # Insert the vote
                cursor.execute("""
                    INSERT INTO Vote (IPAddress, CompetitorID, CompetitionID, VotedBy, VotedAt, Status)
                    VALUES (%s, %s, %s, %s, NOW(), 'active')
                """, (request.remote_addr, competitor_id, competition_id, session['UserID']))
                conn.commit()
                flash('Your vote has been recorded.', 'success')
                return redirect(url_for('results', competition_id=competition_id))
            except mysql.connector.Error as err:
                flash(f"Error: {err}", 'error')
                conn.rollback()
                return redirect(url_for('voting'))

    cursor.close()
    conn.close()

    return render_template('voting.html', competitions=competitions)

@app.route('/results/<int:competition_id>')
def results(competition_id):
    cursor, conn = getCursor(dictionary=True)
    if not cursor or not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('login'))

    cursor.execute("""
        SELECT 
            Competitor.Name AS CompetitorName, 
            COUNT(Vote.VoteID) AS vote_count,
            MAX(Vote.VotedAt) AS LastVoteDateTime,
            Competition.Name AS CompetitionName
        FROM Vote
        JOIN Competitor ON Vote.CompetitorID = Competitor.CompetitorID
        JOIN Competition ON Vote.CompetitionID = Competition.CompetitionID
        WHERE Vote.CompetitionID = %s
        GROUP BY Competitor.Name, Competition.Name
    """, (competition_id,))
    results = cursor.fetchall()

    for result in results:
        if result['LastVoteDateTime']:
            result['LastVoteDate'] = result['LastVoteDateTime'].strftime('%Y-%m-%d')
            result['LastVoteTime'] = result['LastVoteDateTime'].strftime('%H:%M:%S')
        else:
            result['LastVoteDate'] = ''
            result['LastVoteTime'] = ''

    cursor.close()
    conn.close()

    return render_template('voting-result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)