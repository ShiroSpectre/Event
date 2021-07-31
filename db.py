def initialize():
    global bot
    bot = None

    global event_dates
    event_dates = []

    global present_users
    present_users = []

    global alert_time
    alert_time = 900 # 900s = 15min

    global main_channel
    main_channel = 511145993656598540 # 511145993656598540 - main chat | 867707152159342622 - test channel

    global prime_channel
    prime_channel = 533327140574461984 # 533327140574461984 - prime league channel | 867715873417986068 - private test channel

    global last_message_time
    last_message_time = 0

    global last_channel 
    last_channel = None

    global refresh
    refresh = 300 # 300s = 5min

    global mention
    mention = 3600 # 3600s = 1h

    global maybe_reminder
    maybe_reminder = 10800 # 10800s = 3h

    global finish
    finish = 900 # 900s = 15min

    global reminder_role
    reminder_role = 868171992023588934 # 868171992023588934 - termin rolle | 839549248038895636 - testrolle

    global leaderboard_role
    leaderboard_role = 579286739647201296 # 579286739647201296 - rict member | 839549248038895636 - testrolle

    global guild_ID
    guild_ID = 511145993656598538 # 511145993656598538 - rict server | 686147548179595297 - testserver

    global embed_color
    embed_color = 0x00FFB9