class JSONGolferRoundScores(object):
    def __init__(self, tournGolferId, roundId):
        self.model = "golfer.golferroundscores"
        self.fields = {"grs_tourn_golfer": tournGolferId,
                       "grs_round": roundId}


def main():
    standaloneDjango()
    jsonStr = getJSONstr()
    writeJSONstr(jsonStr)


def standaloneDjango():
    import os
    import django
    import json

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wgt_site.settings")
    django.setup()


def getTournID():
    from django.db import models
    from tournament.models import Tournament

    newTournObj = Tournament.objects.get(
        tourn_name="Oak City Championship")
    return newTournObj.tourn_id


def getGolferID(name_to_get):
    from django.db import models
    from golfer.models import Golfer

    newGolfer = Golfer.objects.get(golfer_name=name_to_get)
    return newGolfer.golfer_id


def getTournGolferID(golfer_id, tourn_id):
    from django.db import models
    from golfer.models import TournGolfer
    tourn_golfers = TournGolfer.objects.filter(tg_tourn=tourn_id)
    for tourn_golfer in tourn_golfers:
        if tourn_golfer.tg_golfer.golfer_id == golfer_id:
            tourn_golfer_id = tourn_golfer.tg_id
            break

    return tourn_golfer_id


def getRoundIDs(tourn_id):
    from django.db import models
    from tournament.models import Round

    rounds = Round.objects.filter(round_tourn_id=tourn_id)
    for round_obj in rounds:
        if round_obj.round_day == "Sat":
            round1_id = round_obj.round_id
        else:
            round2_id = round_obj.round_id
    return round1_id, round2_id


def readScores():
    import csv

    golfer_scores_list = []
    input_file = open('golferScores.csv', 'r')
    csv_reader = csv.reader(input_file, delimiter=",")
    for row in csv_reader:
        golfer_scores_list.append(row)

    return golfer_scores_list


def getJSONstr():
    import json
    scores_list = readScores()
    tourn_id = getTournID()
    round1_id, round2_id = getRoundIDs(tourn_id)
    round_scores = []

    for score in scores_list:
        golfer_id = getGolferID(score[0])
        tourn_golfer_id = getTournGolferID(golfer_id, tourn_id)

        if score[2] == 'Sat':
            grs = JSONGolferRoundScores(tourn_golfer_id, round1_id)
        else:
            grs = JSONGolferRoundScores(tourn_golfer_id, round2_id)

        score_list = list(map(int, score[3:]))

        round_score = 0
        j = 1
        for sc in score_list:
            grs.fields["grs_hole{}_score".format(j)] = sc
            round_score = round_score + sc
            j = j + 1

        grs.fields["grs_total_score"] = round_score

        json_grs = json.dumps(grs.__dict__)
        round_scores.append(json_grs)

    jsonStr = str(round_scores).replace("'", '')

    return jsonStr


def writeJSONstr(jsonStr):
    outFile = open('golfer_round_scores_data.json', 'w')
    outFile.write(jsonStr)
    outFile.close()


main()
