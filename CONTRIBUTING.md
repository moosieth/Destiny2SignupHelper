# Contribution Guide for Suraya

Thank you for your interest in contributing to Suraya! This document contains
everything you need to know to get started!

## Overview

Suraya is a Discord Bot that creates and manages Destiny 2 "Looking for Group"
postings. It allows users to coordinate themselves into a group to tackle
Destiny 2's most rewarding activities.

Behind the curtain, Suraya is a Python project. Package management is handled
with [Poetry](https://python-poetry.org/). Eventually, this project will be
deployed within a container, but for now, running natively with Python 3.10+ and
Poetry 1.8.3+ will suffice.

## Conventions

When contributing to this project, please aim to follow the conventions herein.

### Code Formatting

This project is formatted with Black. It's already contained within the Poetry
project, so all you'll need to do is run `python -m poetry run black .`, and
your code will comply with this convention.

### Commits

This project aims to comply with
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Please
ensure your commit messages comply with this standard to the best of your
ability.

### Changelog

Please update the Changelog in accordance with
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Only the owner of this
repository can cut releases, so add any of your modifications into an
`Unreleased` section at the top of the document.

### Code Review

Create a pull request for your branch when your changes are ready for review.

**Keep code reviews professional!** Any feedback given is truly just in an
effort to uphold the quality of the code. The owner(s) of this repository will
try their best to point out when suggestions are optional or preference-based
(and contributors should do the same too!).
