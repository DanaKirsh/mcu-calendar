import pytest
import datetime
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from mcu_calendar.main import *

def test_google_login():
    creds = get_google_creds()
    assert creds


def test_get_movies():
    movies = get_movies()
    assert len(movies) == len(os.listdir(os.path.join('data', 'movies')))


@pytest.mark.parametrize("movie_path", os.listdir(os.path.join('data', 'movies')))
def test_movies_yaml(movie_path):
    movie = Movie.from_yaml(os.path.join('data', 'movies', movie_path))
    assert type(movie.title)        is str
    assert type(movie.release_date) is datetime.date
    assert type(movie.description)  is str


def test_movies_equals():
    movie1 = Movie(title= "MY TITLE", release_date= datetime.date(2019, 4, 20), description= "stuff happens")
    movie2 = Movie(title= "MY TITLE", release_date= datetime.date(2019, 4, 20), description= "stuff happens")
    assert movie1 == movie1
    assert movie1 == movie2
    assert not movie1 != movie2


@pytest.mark.parametrize("movie_dict", [ 
    { "title": "MY TITLE 2", "release_date": datetime.date(2019, 4, 20), "description": "stuff happens"},
    { "title": "MY TITLE", "release_date": datetime.date(2019, 12, 25), "description": "stuff happens"},
    { "title": "MY TITLE", "release_date": datetime.date(2019, 4, 20), "description": "nothing happens"},
])
def test_movies_not_equals(movie_dict):
    movie1 = Movie(title= "MY TITLE", release_date= datetime.date(2019, 4, 20), description= "stuff happens")
    movie2 = Movie(**movie_dict)
    assert movie1 != movie2
    assert not movie1 == movie2


def test_movie_event_equals():
    movie = Movie(title= "MY TITLE", release_date= datetime.date(2019, 4, 20), description= "stuff happens")
    event = {
        "start": { "date": "2019-04-20" },
        "end": { "date": "2019-04-20" },
        "summary": "MY TITLE",
        "description": "stuff happens",
    }
    assert movie == event
    assert event == movie
    assert not movie != event
    assert not event != movie


@pytest.mark.parametrize("event_dict", [ 
    { "start": { "date": "2019-10-20" }, "end": { "date": "2019-04-20" }, "summary": "MY TITLE", "description": "stuff happens" },
    { "start": { "date": "2019-04-20" }, "end": { "date": "2019-03-14" }, "summary": "MY TITLE", "description": "stuff happens" },
    { "start": { "date": "2019-04-20" }, "end": { "date": "2019-04-20" }, "summary": "YOUR TITLE", "description": "stuff happens" },
    { "start": { "date": "2019-04-20" }, "end": { "date": "2019-04-20" }, "summary": "MY TITLE", "description": "Something happens" },
])
def test_movie_event_not_equals(event_dict):
    movie = Movie(title= "MY TITLE", release_date= datetime.date(2019, 4, 20), description= "stuff happens")
    assert movie != event_dict
    assert not movie == event_dict


def test_get_shows():
    shows = get_shows()
    assert len(shows) == len(os.listdir(os.path.join('data', 'shows')))


@pytest.mark.parametrize("show_path", os.listdir(os.path.join('data', 'shows')))
def test_shows_yaml(show_path):
    show = Show.from_yaml(os.path.join('data', 'shows', show_path))
    assert type(show.title)      is str
    assert type(show.start_date) is datetime.date
    assert type(show.weeks)      is int


def test_shows_equals():
    show1 = Show(title= "MY TITLE", start_date= datetime.date(2019, 4, 20), weeks= 7)
    show2 = Show(title= "MY TITLE", start_date= datetime.date(2019, 4, 20), weeks= 7)
    assert show1 == show1
    assert show1 == show2
    assert not show1 != show1
    assert not show1 != show2


@pytest.mark.parametrize("show_dict", [ 
    { "title": "MY TITLE 2", "start_date": datetime.date(2019, 4, 20), "weeks": 3},
    { "title": "MY TITLE", "start_date": datetime.date(2019, 12, 25), "weeks":3},
    { "title": "MY TITLE", "start_date": datetime.date(2019, 4, 20), "weeks": 9},
])
def test_shows_not_equals(show_dict):
    show1 = Show(title= "MY TITLE", start_date= datetime.date(2019, 4, 20), weeks= 3)
    show2 = Show(**show_dict)
    assert not show1 == show2
    assert show1 != show2


def test_show_event_equals():
    show = Show(title= "MY TITLE", start_date= datetime.date(2019, 4, 20), weeks= 20)
    event = {
        "start": { "date": "2019-04-20" },
        "end": { "date": "2019-04-21" },
        "summary": "MY TITLE",
        "recurrence": [f"RRULE:FREQ=WEEKLY;WKST=SU;COUNT=20;BYDAY=SA"],
    }
    assert show == event
    assert event == show
    assert not show != event
    assert not event != show


@pytest.mark.parametrize("event_dict", [ 
    { "start": { "date": "2019-10-20" }, "end": { "date": "2019-04-21" }, "summary": "MY TITLE", "recurrence": f"RRULE:FREQ=WEEKLY;WKST=SU;COUNT=6;BYDAY=SA" },
    { "start": { "date": "2019-04-20" }, "end": { "date": "2019-03-14" }, "summary": "MY TITLE", "recurrence": f"RRULE:FREQ=WEEKLY;WKST=SU;COUNT=6;BYDAY=SA" },
    { "start": { "date": "2019-04-20" }, "end": { "date": "2019-04-21" }, "summary": "YOUR TITLE", "recurrence": f"RRULE:FREQ=WEEKLY;WKST=SU;COUNT=6;BYDAY=SA" },
    { "start": { "date": "2019-04-20" }, "end": { "date": "2019-04-21" }, "summary": "MY TITLE", "recurrence": f"RRULE:FREQ=WEEKLY;WKST=SU;COUNT=10;BYDAY=SA" },
])
def test_show_event_not_equals(event_dict):
    show = Show(title= "MY TITLE", start_date= datetime.date(2019, 4, 20), weeks= 6)
    assert not show == event_dict
    assert show != event_dict
