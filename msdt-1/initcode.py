import json
import feedparser
import bs4


import telegram
import telegram.ext

BOT_TOKEN = "243527010:AAGWz1pfH5uIKOFAH2A6M6wwIoVdhwhjxzY"
updater = telegram.ext.Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
job_queue = updater.job_queue


def check_feed_updates():
    """
    Checks if feeds have updated by comparing saved feed dates to new feed dates.
    """
    try:
        with open("feeds.txt") as feed_file:
            saved_feeds = json.load(feed_file)
        updates = {}

        current_english_update = feedparser.parse(
            "http://rss.weather.gov.hk/rss/CurrentWeather.xml"
        )
        warning_english_update = feedparser.parse(
            "http://rss.weather.gov.hk/rss/WeatherWarningBulletin.xml"
        )

        if current_english_update:
            current_english_feed = saved_feeds["current"][0]
            if current_english_feed["entries"][0]["published"] != current_english_update.entries[0].published:
                current_traditional_update = feedparser.parse(
                    "http://rss.weather.gov.hk/rss/CurrentWeather_uc.xml"
                )
                current_simplified_update = feedparser.parse(
                    "http://gbrss.weather.gov.hk/rss/CurrentWeather_uc.xml"
                )
                current_update = [
                    current_english_update, current_traditional_update, current_simplified_update
                ]
                updates["current"] = current_update
                saved_feeds["current"] = current_update

        if warning_english_update:
            warning_english_feed = saved_feeds["warning"][0]
            if warning_english_feed["entries"][0]["published"] != warning_english_update.entries[0].published:
                warning_traditional_update = feedparser.parse(
                    "http://rss.weather.gov.hk/rss/WeatherWarningBulletin_uc.xml"
                )
                warning_simplified_update = feedparser.parse(
                    "http://gbrss.weather.gov.hk/rss/WeatherWarningBulletin_uc.xml"
                )
                warning_update = [
                    warning_english_update, warning_traditional_update, warning_simplified_update
                ]
                updates["warning"] = warning_update
                saved_feeds["warning"] = warning_update

    except FileNotFoundError:
        current_english_feed = feedparser.parse(
            "http://rss.weather.gov.hk/rss/CurrentWeather.xml"
        )
        current_traditional_feed = feedparser.parse(
            "http://rss.weather.gov.hk/rss/CurrentWeather_uc.xml"
        )
        current_simplified_feed = feedparser.parse(
            "http://gbrss.weather.gov.hk/rss/CurrentWeather_uc.xml"
        )
        current_feeds = [
            current_english_feed, current_traditional_feed, current_simplified_feed
        ]

        warning_english_feed = feedparser.parse(
            "http://rss.weather.gov.hk/rss/WeatherWarningBulletin.xml"
        )
        warning_traditional_feed = feedparser.parse(
            "http://rss.weather.gov.hk/rss/WeatherWarningBulletin_uc.xml"
        )
        warning_simplified_feed = feedparser.parse(
            "http://gbrss.weather.gov.hk/rss/WeatherWarningBulletin_uc.xml"
        )
        warning_feeds = [
            warning_english_feed, warning_traditional_feed, warning_simplified_feed
        ]

        with open("feeds.txt", "w") as feed_file:
            updates = {"current": current_feeds, "warning": warning_feeds}
            saved_feeds = updates
            json.dump(updates, feed_file)

    if updates:
        with open("feeds.txt", "w") as feed_file:
            json.dump(saved_feeds, feed_file)
    return updates


def get_user_language_preferences():
    """
    Returns language preferences for all users.
    """
    try:
        with open("user_language.txt") as language_file:
            user_language_preferences = json.load(language_file)
    except FileNotFoundError:
        user_language_preferences = {}
    return user_language_preferences


def get_available_topics():
    """
    Returns a list of available topics.
    """
    topics = ["Current - Current weather information",
              "Warning - Warnings in force"]
    topics_message = "The topics I can tell you about are:\n" + "\n".join(topics)
    return topics_message


def get_feed_message_for_user(user_id, topic):
    """
    Returns the formatted feed in the user's preferred language.
    """
    check_feed_updates()
    user_language_preferences = get_user_language_preferences()
    language = user_language_preferences.get(user_id, "english")
    with open("feeds.txt") as feed_file:
        saved_feeds = json.load(feed_file)

    if language == "english":
        selected_feed = saved_feeds[topic][0]
    elif language == "traditional":
        selected_feed = saved_feeds[topic][1]
    elif language == "simplified":
        selected_feed = saved_feeds[topic][2]

    formatted_feed = bs4.BeautifulSoup(selected_feed["entries"][0]["summary"], "html.parser")
    if topic == "current":
        for line_break in formatted_feed.find_all("br"):
            if line_break.previous_element != line_break:
                line_break.previous_element.wrap(formatted_feed.new_tag("p"))
            line_break.decompose()
        for table_row in formatted_feed.find_all("tr"):
            table_row.decompose()
        for span_element in formatted_feed.find_all("span"):
            span_element.decompose()
        for table_element in formatted_feed.find_all("table"):
            if table_element.find_previous("p") != formatted_feed.p:
                table_element.find_previous("p").decompose()
            table_element.decompose()
        message_parts = []
        for text_string in formatted_feed.stripped_strings:
            message_parts.append(" ".join(text_string.split()))
        message = "\n".join(message_parts)

    elif topic == "warning":
        message = formatted_feed.get_text()
    return message


def start_bot(bot, update):
    """
    Handles the /start command.
    """
    message = "Hi, I'm HKObservatoryBot! Type @hkobservatory_bot to see what I can do!"
    bot.sendMessage(chat_id=update.message.chat_id, text=message)


def handle_inline_query(bot, update):
    """
    Handles inline queries from the user.
    """
    query = update.inline_query.query
    results = []
    user_id = str(update.inline_query.from_user.id)
    user_first_name = update.inline_query.from_user.first_name

    if not query:
        results.append(
            telegram.InlineQueryResultArticle(
                id="commands",
                title="Commands",
                input_message_content=telegram.InputTextMessageContent(
                    ("Type @hkobservatory_bot + one of the following:\n""topics;"
                     "\ntellme + topic;\nsubscribe + topic;\nunsubscribe + topic;"
                     "\nenglish;\n繁體中文;\n简体中文;")),
                description="List of available commands"
            )
        )
    else:
        if query.lower() in "topics":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="topics",
                    title="Topics",
                    input_message_content=telegram.InputTextMessageContent(
                        get_available_topics()
                    ),
                    description="List of available topics"
                )
            )
        if query.lower() in "tellme current":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="tellme_current",
                    title="Current Weather",
                    input_message_content=telegram.InputTextMessageContent(
                        get_feed_message_for_user(user_id, "current")
                    ),
                    description="Current weather from the HK Observatory"
                )
            )
        if query.lower() in "tellme warning":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="tellme_warning",
                    title="Warning",
                    input_message_content=telegram.InputTextMessageContent(get_feed_message_for_user(user_id, "warning")),
                    description="Warnings in force"
                )
            )
        if query.lower() in "subscribe current":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="sub_current",
                    title="Subscribe Current",
                    input_message_content=telegram.InputTextMessageContent(
                        user_first_name + " has subscribed to: Current"
                    ),
                    description="Subscribe to current to receive updates"
                )
            )
        if query.lower() in "subscribe warning":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="sub_warning",
                    title="Subscribe Warning",
                    input_message_content=telegram.InputTextMessageContent(
                        user_first_name + " has subscribed to: Warning"
                    ),
                    description="Subscribe to warning to receive updates"
                )
            )
        if query.lower() in "unsubscribe current":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="unsub_current",
                    title="Unsubscribe Current",
                    input_message_content=telegram.InputTextMessageContent(
                        user_first_name + " has unsubscribed from: Current"
                    ),
                    description="Unsubscribe from current to stop receiving updates"
                )
            )
        if query.lower() in "unsubscribe warning":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="unsub_warning",
                    title="Unsubscribe Warning",
                    input_message_content=telegram.InputTextMessageContent(
                        user_first_name + " has unsubscribed from: Warning"
                    ),
                    description="Unsubscribe from warning to stop receiving updates"
                )
            )
        if query.lower() in "english":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="lang_english",
                    title="English",
                    input_message_content=telegram.InputTextMessageContent(
                        user_first_name + "\'s language changed to English"
                    ),
                    description="Select English as topic information language"
                )
            )
        if query in "繁體中文":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="lang_traditional",
                    title="繁體中文",
                    input_message_content=telegram.InputTextMessageContent(
                        user_first_name + "\'s language changed to 繁體中文"
                    ),
                    description="Select 繁體中文 as topic information language"
                )
            )
        if query in "简体中文":
            results.append(
                telegram.InlineQueryResultArticle(
                    id="lang_simplified",
                    title="简体中文",
                    input_message_content=telegram.InputTextMessageContent(
                        user_first_name + "\'s language changed to 简体中文"
                    ),
                    description="Select 简体中文 as topic information language"
                )
            )
    bot.answerInlineQuery(update.inline_query.id, results, cache_time=0)


def handle_inline_result(bot, update):
    """
    Saves language preferences and subscriptions.
    """
    result_id = update.chosen_inline_result.result_id
    user_id = str(update.chosen_inline_result.from_user.id)

    if "lang" in result_id:
        language = result_id[5:]
        try:
            with open("user_language.txt") as language_file:
                user_language_preferences = json.load(language_file)
        except FileNotFoundError:
            user_language_preferences = {}

        with open("user_language.txt", "w") as language_file:
            if result_id == ("lang_" + language):
                user_language_preferences[user_id] = language
            json.dump(user_language_preferences, language_file)

    elif "sub" in result_id:
        topic = result_id[4:]
        try:
            with open("subscribers.txt") as subscribers_file:
                subscribers = json.load(subscribers_file)
        except FileNotFoundError:
            subscribers = {}

        with open("subscribers.txt", "w") as subscribers_file:
            if result_id == ("sub_" + topic):
                try:
                    if user_id not in subscribers[topic]:
                        subscribers[topic].append(user_id)
                except KeyError:
                    subscribers[topic] = [user_id]
            elif result_id == ("unsub_" + topic):
                try:
                    subscribers[topic].remove(user_id)
                except:
                    pass
            json.dump(subscribers, subscribers_file)


def send_updates_to_subscribers(bot, job):
    """
    Sends updates to subscribed users.
    """
    try:
        with open("subscribers.txt") as subscribers_file:
            subscribers = json.load(subscribers_file)
        user_language_preferences = get_user_language_preferences()
    except FileNotFoundError:
        subscribers = {}

    if subscribers:
        updates = check_feed_updates()
        if updates:
            for topic in updates:
                try:
                    for user_id in subscribers[topic]:
                        language = user_language_preferences.get(user_id, "english")
                        message = get_feed_message_for_user(updates, topic, language)
                        bot.sendMessage(chat_id=user_id, text=message)
                except telegram.Unauthorized:
                    subscribers[topic].remove(user_id)
                except:
                    pass


# Bot will check for updates every hour
job_queue.put(telegram.ext.Job(send_updates_to_subscribers, 3600.0))

# Handlers for commands, inline queries and results
start_handler = telegram.ext.CommandHandler("start", start_bot)
dispatcher.add_handler(start_handler)

inline_query_handler = telegram.ext.InlineQueryHandler(handle_inline_query)
dispatcher.add_handler(inline_query_handler)

inline_result_handler = telegram.ext.ChosenInlineResultHandler(handle_inline_result)
dispatcher.add_handler(inline_result_handler)

updater.start_polling()
updater.idle()
updater.start_polling()
updater.idle()
