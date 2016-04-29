#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import psycopg2.extensions
from psycopg2.extensions import b
# we have to import the Psycopg2 extras library!
import psycopg2.extras
import sys
import collections
import itertools
from random import sample, choice, randrange
from operator import itemgetter, mul
from itertools import starmap, repeat, chain, cycle, tee, \
    groupby, count, combinations, starmap, islice
try:
    from itertools import imap as map, izip as zip, ifilter as filter, \
        izip_longest as zip_longest, ifilterfalse as filterfalse
except ImportError as err:
    from itertools import zip_longest, filterfalse
    

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # We make use of the connect() method so that we could avoid the code repetition.
    # We can refactor our connect() method to deal not only with the database connection
    # but also with the cursor since we can assign and return multiple variables simultaneously.
    # In the stage of setting up the connection with the DB, sometimes we may encounter different exceptions.
    # In practice, we handle this crucial stage carefully by using try/except block.
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error when connecting the server")

    
def deleteMatches():
    """Remove all the match records from the database."""
    db = psycopg2.connect("dbname=tournament")
    c = db.cursor()

    query = "TRUNCATE matches;"
    c.execute(query)

    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()

    query = "DELETE FROM players;"
    c.execute(query)

    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()

    query = "SELECT count(*) AS num FROM players;"
    c.execute(query)
    count = cur.fetchone()[0]

    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player. (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
    name: the player's full name (need not be unique).
    """
    db, cursor = connect()

    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    c.execute(query, parameter)

    db.commit()
    db.close()
    
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
    A list of tuples, each of which contains (id, name, wins, matches):
    id: the player's unique id (assigned by the database)
    name: the player's full name (as registered)
    wins: the number of matches the player has won
    matches: the number of matches the player has played
    """
    db, cursor = connect()
    
    c.execute("SELECT * FROM standings ODER BY wins DESC;")
    playerslist = c.fetchall() #Fetches all remaining rows of a query result, returning a list.

    db.close()
    return playerslist

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
    winner: the id number of the player who won
    loser: the id number of the player who lost
    """
    db = cursor.connect()
    
    query = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s);"
    parameter = (winner, loser)
    c.execute(query, parameter)

    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2),
      first player's unique id
      name1: the first player's name
      id2: the second player's unique id
      name2: the second player's name
    """
    # For swissPairings consulted GitHub, Stack OverFlow
    # and the recipes section of Python's
    # itertools docs: https://docs.python.org/2/library/itertools.html
    # and the Python Standard Library.

    # Iterate through the list and build the pairings to return results
    results = []
    pair = []
    standings = playerStandings()
    # standings = [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)]
    # [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    # pairings = swissPairings()
    pairingsiterator = itertools.izip(*[iter(standings)]*2)
    pairings = list(pairingsiterator)
    for pair in pairings:
        id1 = pair[0][0]
        name1 = pair[0][1]
        id2 = pair[1][0]
        name2 = pair[1][1]
        matchup = (id1, name1, id2, name2)
        results.append(matchup)
    return results
