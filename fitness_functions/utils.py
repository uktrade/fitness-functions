import datetime


def check_last_collection(connection, minimum_time_seconds=30):
    # Very hacky way to stop this from being executed over and over again in pre-commit hooks
    with connection:
        cur = connection.cursor()
        cur.execute("""
                    SELECT * 
                    FROM FITNESS_METRICS 
                    WHERE rowid = (SELECT MAX(rowid) FROM FITNESS_METRICS);
                """)
        latest_record = cur.fetchone()
        latest_datetime = datetime.datetime.fromisoformat(latest_record[1])
        if (datetime.datetime.now() - latest_datetime).seconds < minimum_time_seconds:
            # Basically we can't run this twice within x seconds
            print(f"Fitness Functions ran within last {minimum_time_seconds } seconds, ignoring")
            return False
        return True

