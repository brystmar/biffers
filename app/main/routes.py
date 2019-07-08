from app import logger
from app.main import bp
from app.main.forms import BifSelector, ScrapeNewThread, ScrapeExistingThread, UpdateLikes, CustomOutput
from flask import render_template, redirect, url_for, request, send_from_directory
from main import db
import boto3

URLs = None


@bp.route('/')
@bp.route('/index')
@bp.route('/browse', methods=['GET', 'POST'])
def browse():
    logger.debug("Start of browse()")

    # Retrieve all known threads from the database
    threads = scan_table('biffers_thread')

    bifs = to_choices_list(threads)
    bif_selection = BifSelector()
    bif_selection.selector.choices = bifs

    scrape_new_thread_form = ScrapeNewThread()
    scrape_existing_thread_form = ScrapeExistingThread()
    likes_form = UpdateLikes()
    output_form = CustomOutput()

    if scrape_existing_thread_form.validate_on_submit():
        logger.debug("Clicked the ScrapeExistingThread button")

        scrape_existing_thread(bif_selection.selector.data)
        return redirect(url_for("main.browse"))

    elif scrape_new_thread_form.validate_on_submit():
        logger.debug("Clicked the ScrapeNewThread button")

        # VALIDATION #
        # Desired thread name must be unique
        if scrape_new_thread_form.thread_name.data.lower() in list_to_lowercase(bifs, 'name'):
            logger.debug("Desired BIF name already exists")
            return redirect(url_for("main.browse"))

        # URL must also be unique
        if scrape_new_thread_form.url.data.lower() in list_to_lowercase(bifs, 'url'):
            logger.debug("Duplicate thread -- URL already exists")
            return redirect(url_for("main.browse"))

        # Gather the high-level thread details

        scrape_new_thread(scrape_new_thread_form.thread_name.data, scrape_new_thread_form.url.data)
        return redirect(url_for("main.browse"))

    elif likes_form.validate_on_submit():
        logger.debug("Clicked the UpdateLikes button")

        update_likes(bif_selection.selector.data)
        return redirect(url_for("main.browse"))

    elif output_form.validate_on_submit():
        logger.debug("Clicked the CustomOutput button")

        create_custom_html_output(bif_selection.selector.data)
        return redirect(url_for("main.browse"))

    return render_template('browse.html', title='Browse TalkBeer BIFs', bif_data=threads,
                           bif_selection=bif_selection, scrape_existing_thread_button=scrape_existing_thread_form,
                           likes_button=likes_form, output_button=output_form)


def scan_table(table) -> list:
    """Scan the requested table, log response info as needed, return the data."""
    response = db.Table(table).scan()

    # Check the response code
    response_code = response['ResponseMetadata']['HTTPStatusCode']
    logger.debug(f"Scanned the {table} table, HTTPStatusCode={response_code}")
    if response_code == 200:
        logger.debug(f"{response['Count']} threads returned from dynamodb")
    else:
        logger.warning(f"DynamoDB error: HTTPStatusCode={response_code}")
        logger.warning(f"Full response log:\n{response['ResponseMetadata']}")
    return response['Items']


def to_choices_list(data) -> list:
    """Return a sorted list of key/value tuples that identifies each BIF."""
    sorted_list = []
    other_bifs = []
    for d in data:
        # Keep the SSF BIFs at the top
        if 'ssf' in d['name'].lower():
            sorted_list.append((d['name'], d['name']))
        else:
            other_bifs.append((d['name'], d['name']))

    sorted_list.sort()
    other_bifs.sort()

    for o in other_bifs:
        sorted_list.append(o)

    return sorted_list


def list_to_lowercase(data, key) -> list:
    """Return a sorted list of key/value tuples that identifies each BIF."""
    lower_list = []
    for d in data:
        lower_list.append(d[key].lower())
    return lower_list


def scrape_existing_thread(thread_name):
    """Scrape data for a thread that already exists in our database."""
    logger.debug(f"Start of scrape_existing_thread for {thread_name}")

    logger.debug("End of scrape_existing_thread")


@bp.route('/scrape_new_thread')
def scrape_new_thread(thread_name, url):
    """Scrape data for a thread that isn't already in our database."""
    logger.debug(f"Start of scrape_new_thread for {thread_name}, {url}")

    # URL Validation

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
