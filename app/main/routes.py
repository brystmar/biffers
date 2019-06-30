from app import logger
from app.main import bp
from app.main.forms import BifSelector, ScrapeExistingThread, UpdateLikes, CustomOutput
from flask import render_template, redirect, url_for, request, send_from_directory
import boto3


@bp.route('/')
@bp.route('/index')
@bp.route('/browse', methods=['GET', 'POST'])
def browse():
    logger.debug("Start of browse()")
    bif_data = [dict(name="SSF002", ongoing=0, start_date="2012-02-04", end_date="2012-05-28",
                     url="http://www.talkbeer.com/SSF002", organizer_id=229),
                dict(name="SSF001", ongoing=0, start_date="2011-01-23", end_date="2011-04-19",
                     url="http://www.talkbeer.com/SSF001", organizer_id=37),
                dict(name="SSF003", ongoing=1, start_date="2013-09-17", end_date="2013-12-14",
                     url="http://www.talkbeer.com/SSF003", organizer_id=2051)
                ]

    bif_selection = BifSelector()
    bif_selection.selector.choices = to_choices_list(bif_data)

    scrape_existing_thread_form = ScrapeExistingThread()
    likes_form = UpdateLikes()
    output_form = CustomOutput()

    if scrape_existing_thread_form.validate_on_submit():
        logger.debug("Clicked the ScrapeExistingThread button")

        scrape_existing_thread(bif_selection.selector.data)
        return redirect(url_for("main.browse"))

    elif scrape_new_thread_form.validate_on_submit():
        logger.debug("Clicked the ScrapeNewThread button")

        scrape_new_thread(bif_selection.selector.data)
        return redirect(url_for("main.browse"))

    elif likes_form.validate_on_submit():
        logger.debug("Clicked the UpdateLikes button")

        update_likes(bif_selection.selector.data)
        return redirect(url_for("main.browse"))

    elif output_form.validate_on_submit():
        logger.debug("Clicked the CustomOutput button")

        create_custom_html_output(bif_selection.selector.data)
        return redirect(url_for("main.browse"))

    return render_template('browse.html', title='Browse TalkBeer BIFs', bif_data=bif_data, bif_selection=bif_selection,
                           scrape_existing_thread_button=scrape_existing_thread_form, likes_button=likes_form,
                           output_button=output_form)


def to_choices_list(data) -> list:
    """Return a sorted list of key/value tuples that identifies each BIF."""
    sorted_list = []
    for d in data:
        sorted_list.append((d['name'], d['name']))

    sorted_list.sort()
    return sorted_list


def scrape_existing_thread(thread_name):
    """Scrape data for a thread that already exists in our database."""
    logger.debug(f"Start of scrape_existing_thread for {thread_name}")

    logger.debug("End of scrape_existing_thread")


@bp.route('/scrape_new_thread')
def scrape_new_thread(thread_name="abc"):
    """Scrape data for a thread that isn't already in our database."""
    logger.debug(f"Start of scrape_new_thread for {thread_name}")

    # TODO: write this function, then hand it off to scrape_existing_thread()
    logger.debug("Now that the thread exists in our db, hand it off to scrape_existing_thread()")
    scrape_existing_thread(thread_name)
    logger.debug("End of scrape_new_thread")

    return render_template('scrape_new_thread.html', title='Browse TalkBeer BIFs')


def update_likes(thread_name):
    """Update likes for recent posts."""
    logger.debug(f"Start of update_likes for {thread_name}")


def create_custom_html_output(thread_name):
    """Aggregate posts for the selected thread in a different way, according to pre-defined options."""
    logger.debug(f"Start of create_custom_html_output for {thread_name}")
