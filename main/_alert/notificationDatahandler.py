from _alert.telegramBot import TelegramBot
from _database.sqliteConnector import plutus
from configReader import configExtract

class NotificationHandler():
    botty = TelegramBot()
    conf = configExtract("environment.json").conf
    
    
    def notifyTelegram(self):
        
        channel = self.conf['telegramChat']
        token = self.conf['telegramToken']
        
        db = plutus()
        
        db.connect()
        
        diffs = db.getDiffs(db.getNewBatchID('diff')-1)
        
        for row in diffs:
            
            message = self.createText(row)
            
            if db.addNotification(message=message, plattform="Telegram", destination=f"{channel}") == -1:
                continue
            
            self.botty.sendMessage(chat=channel, token=token, message=message)
        
        db.closeConnection()
        
    #def createText(self, summary, location, description, date, start, end ):
    #    date = f"{date.split('-')[2]}.{date.split('-')[1]}.{date.split('-')[0]}"
    #    return f"<b>{summary}</b>\n<b>Raum:</b> {location}\n<b>Stunde</b>: {date} {start}-{end}\n<b>Beschreibung:</b> {description}"


    def createText(self, diff_row: dict) -> str:
        """
        Build a Telegram-ready HTML message based on a row from the `diff` table.

        Always include:
          - name, newDate, newEnd, newState (if present)

        Additionally include only those fields where BOTH the corresponding oldX and newX
        values are present (non-empty). Supported fields come from setup/sql/createDiff.sql:
          old/new: Date, Start, End, State, StateDetail, Room, Subject, Text.

        Args:
          name: Human-readable name/summary for the entry (e.g., lesson title).
          diff_row: Mapping with keys like 'oldDate', 'newDate', 'oldRoom', 'newRoom', etc.

        Returns:
          HTML string formatted for Telegram messages (parse_mode=HTML).
        """

        def _has_value(v) -> bool:
            return v is not None and str(v).strip() != ""

        def _escape(s: str) -> str:
            # Minimal HTML escaping for Telegram HTML parse mode
            return (
                str(s)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

        def _fmt_date(d: str) -> str:
            try:
                y, m, day = d.split("-")
                return f"{day}.{m}.{y}"
            except Exception:
                return d

        # Header: name, state, date/time
        lines = []
        name = diff_row.get("newSubject", "")
        if _has_value(name):
            lines.append(f"<b>{_escape(name)}</b>")

        new_state = diff_row.get("newState", "")
        if _has_value(new_state):
            lines.append(f"<b>Status:</b> {_escape(new_state)}")

        new_date = diff_row.get("newDate", "")
        new_end = diff_row.get("newEnd", "")
        if _has_value(new_date):
            lines.append(f"<b>Date:</b> {_fmt_date(new_date)}")
        if _has_value(new_end):
            lines.append(f"<b>Ends:</b> {_escape(new_end)}")

        # Changes: only fields where both oldX and newX exist and are non-empty
        changes = []
        fields = [
            ("Date", "oldDate", "newDate"),
            ("Start", "oldStart", "newStart"),
            ("End", "oldEnd", "newEnd"),
            ("State", "oldState", "newState"),
            ("State detail", "oldStateDetail", "newStateDetail"),
            ("Room", "oldRoom", "newRoom"),
            ("Subject", "oldSubject", "newSubject"),
            ("Text", "oldText", "newText"),
        ]

        for label, old_key, new_key in fields:
            old_val = diff_row.get(old_key, "")
            new_val = diff_row.get(new_key, "")
            if _has_value(old_val) and _has_value(new_val):
                # Reuse date formatting for Date field
                if label == "Date":
                    old_val_fmt = _fmt_date(str(old_val))
                    new_val_fmt = _fmt_date(str(new_val))
                    changes.append(f"• <b>{label}:</b> {_escape(old_val_fmt)} → {_escape(new_val_fmt)}")
                else:
                    changes.append(f"• <b>{label}:</b> {_escape(old_val)} → {_escape(new_val)}")

        if changes:
            lines.append("<b>Changes:</b>")
            lines.extend(changes)

        return "\n".join(lines)