#!/usr/bin/env python3
from flask import jsonify
from flask_classful import FlaskView
from datetime import datetime
import tzlocal
from sqlalchemy import text

from utils import apikey_required

from model import db


class PlayerdataView(FlaskView):
    decorators = [apikey_required(False)]

    def index(self):
        statement = text("""SELECT DISTINCT `supp`.`playername`, `supp`.`time`, `supp`.`type` = 'join' AS online 
            FROM (SELECT `playername`, MAX(`time`) AS `time` 
                  FROM `playerlogger` 
                  WHERE `type` IN ('join', 'quit') 
                  GROUP BY `playername`
                 ) `orig` 
            JOIN `playerlogger` `supp` 
            ON `orig`.`playername` = `supp`.`playername` AND `orig`.`time` = `supp`.`time` 
            WHERE `supp`.`type` IN ('join', 'quit') 
            ORDER BY `time` DESC;""")

        result = [
            {
                "name": ply["playername"],
                # Converts to given timezone automagically
                "last_seen": datetime.fromtimestamp(ply["time"], tz=tzlocal.get_localzone()),
                "online": bool(ply["online"])}
            for ply in db.engine.execute(statement)
        ]

        return jsonify(result)
