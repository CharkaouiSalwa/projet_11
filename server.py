import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import  datetime



def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        email = request.form['email']
        club = next((club for club in clubs if club['email'] == email), None)
        if club is not None:
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash("Sorry, that email wasn't found.")
            return redirect(url_for('index'))
    except Exception as e:
        flash("An error occurred. Please try again.")
        return redirect(url_for('index'))




@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition and foundCompetition['date'] >= str(datetime.now()):
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, date=str(datetime.now()))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition_name = request.form['competition']
        club_name = request.form['club']
        places_required = int(request.form['places'])

        # Trouver la compétition et le club correspondants dans les listes
        competition = next((c for c in competitions if c['name'] == competition_name), None)
        club = next((c for c in clubs if c['name'] == club_name), None)

        if competition is None or club is None:
            flash("Club or competition not found.")
        else:
            # Convertir le nombre de points du club en entier
            club_points = int(club['points'])
            competition_place = int(competition['numberOfPlaces'])
            # Vérifier si le nombre de places demandées dépasse le maximum de 12
            if places_required > 12:
                flash("You can only book up to 12 places.")
            #  éviter que le club ne réserve plus de places qu'il n'a de points disponibles
            elif club_points < places_required:
                flash("Not enough points to make the booking.")
            else:
                # Vérifier si le club a suffisamment de points pour réserver
                if club_points >= places_required:
                    # Déduire le nombre de places réservées de la compétition
                    competition_place -= places_required
                    competition['numberOfPlaces'] = str(competition_place)
                    # Déduire les points du club
                    club_points -= places_required
                    club['points'] = str(club_points)
                    flash('Booking complete! Number of places purchased: ' + str(places_required))
                else:
                    flash("Not enough points to make the booking.")

        return render_template('welcome.html', club=club, competitions=competitions)
    except Exception as e:
        flash("An error occurred. Please try again.")
        return redirect(url_for('index'))


# TODO: Add route for points display
@app.route('/points_display')
def points_display():
    return render_template('points_display.html', clubs=clubs)



@app.route('/logout')
def logout():
    return redirect(url_for('index'))