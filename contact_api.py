#! /usr/bin/python3
""" Gets all weekly artist charts for given user and
stores it as json into chart_week_<timestamp> file """
import sys
import requests

ROOT_API_URL = "http://ws.audioscrobbler.com/2.0/"
API_KEY = "API_KEY"
USER_URL_OPTIONS = "?method={}&user={}&api_key={}&format=json"
EXTENDED_OPTIONS = "&from={}&to={}"


def get_all_available_charts_for_user(user):
    """ Get all available charts for given user, of which some may be empty (wtf lastfm?) """
    available_weekly_charts_request = \
        requests.get(
            ROOT_API_URL + USER_URL_OPTIONS.format("user.getWeeklyChartList", user, API_KEY)
        )

    available_weekly_charts_json = available_weekly_charts_request.json()

    return available_weekly_charts_json


def extract_user_charts(available_weekly_charts_json, user):
    """ Get all available user charts from list of available user charts.
    Again, some may be empty """
    for potential_chart in available_weekly_charts_json['weeklychartlist']['chart']:
        request_url = ROOT_API_URL + USER_URL_OPTIONS.format(
            "user.getWeeklyArtistChart", user, API_KEY) \
            + EXTENDED_OPTIONS.format(potential_chart["from"], potential_chart["to"])
        weekly_chart = requests.get(request_url)
        weekly_chart_data = weekly_chart.json()

        yield weekly_chart_data


def write_all_artist_info_to_file(user_charts, output_folder="."):
    """ write all artist info to file(s) """
    for user_chart in user_charts:
        if user_chart["weeklyartistchart"]["artist"]:
            week_start = user_chart["weeklyartistchart"]["@attr"]["from"]
            with open('{}/chart_week_{}'.format(output_folder, week_start), 'w') as out_file:
                out_file.write(str(user_chart["weeklyartistchart"]))
                print(week_start)


if __name__ == "__main__":
    username = sys.argv[1]

    folder = None
    if sys.argv[2]:
        folder = sys.argv[2]

    available_charts = get_all_available_charts_for_user(username)

    extracted_user_charts = extract_user_charts(available_charts, username)

    write_all_artist_info_to_file(extracted_user_charts, folder)
