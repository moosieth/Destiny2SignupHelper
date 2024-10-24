# Suraya

An open-source discord bot with features to promote group coordination and
sign-up for Destiny 2 activities.

[Click here to add Suraya to your server!](https://discord.com/oauth2/authorize?client_id=1245532850351112252&permissions=8&response_type=code&redirect_uri=https%3A%2F%2Fmoosieth.github.io%2F&integration_type=0&scope=bot+applications.commands+guilds.join)

## Running

If you want to stand up your own instance of Suraya, follow the instructions
contained in this section.

### Prerequisites

To run Suraya, you'll need:

- Python 3.10+
- Poetry 1.8.3+

You'll also need to create a `.env` file within this directory that defines the
following variables:

- `MONGO_URI`: The URI for a MongoDB deployment
- `TOKEN`: A private token for a Discord Application
- `OWNER_ID`: Your Discord User ID. Needed so you can use `!sync` to sync the
  slash commands. _Note that this is not your username, but rather, your unique
  Discord interger ID._

## Using Suraya

Currently, Suraya has the following available commands:

- `/lfg-raid`: Creates an LFG posting for a Raid activity. Its arguments are:
  - `activity`: The name of the Raid you're making the posting for
  - `needed`: The number of players you need
  - `description`: A description of your posting. This should contain any info
    you want potential applicants to know.
  - `time`: The time you want to start the activity. This should be of the
    format `HH:MM{a|p}`.
- `/lfg-dungeon`: Creates an LFG posting for a Dungeon activity
  - `activity`: The name of the Dungeon you're making the posting for
  - `needed`: The number of players you need
  - `description`: A description of your posting. This should contain any info
    you want potential applicants to know.
  - `time`: The time you want to start the activity. This should be of the
    format `HH:MM{a|p}`.
- `/help`: Display a help message detailing these commands and their arguments

## Future Enhancements

- Soon, Suraya will create a Discord Thread for each posting, so that
  participants can communicate beforehand
- Soon, Suraya will notify all participants of a posting at a pre-determined
  time before the activity starts.
- Soon, Suraya will be able to store default behaviors for each Discord server
  it is in, such as a default Time Zone for postings, notification preferences,
  and more.
- **STRETCH GOAL**: We'd like to make Suraya use the Bungie API, so that it can
  track activity completions and award "Guided Games"-esque trophies and stats.
