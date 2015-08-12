#!/usr/bin/env python

import errno, sys, json, urllib2, click, os.path

@click.command()

@click.argument('command')
@click.argument('url')

@click.option('--file', '-f')
@click.option('--title', '-t')
@click.option('--description', '-d')
@click.option('--message', '-m')
@click.option('--type', type=click.Choice(['INFO', 'ARTIFACT', 'WARNING']), default='INFO')
@click.option('--link', '-l', multiple=True, type=(unicode, unicode, unicode))

def main(file, title, description, message, type, link, command, url):

    if command == 'init':
        if os.path.isfile(file):
            with open(file) as data_file:
                data = json.load(data_file)
        data['title'] = title
        data['description'] = description
        req = urllib2.Request(url + "/pipeline/init")
        req.add_header('Content-Type', 'application/json')
        urllib2.urlopen(req, json.dumps(data))
        click.echo("Initialize successfull!")

    if command == 'progress':
        urllib2.urlopen(url + "/pipeline/progress").read()
        click.echo("A progress was made!")

    if command == 'fail':
        urllib2.urlopen(url + "/pipeline/fail").read()
        click.echo("Pipeline set to failure!")

    if command == 'archive':
        targets = {url + "/pipeline/get":"pipeline.json",
                    url + "/pipevis.html":"pipevis.html",
                    url + "/pipevis.style.css":"pipevis.style.css",
                    url + "/pipevis.app.js":"pipevis.app.js",
                    url + "/logo_giphy.png":"logo_giphy.png" }
        for target_url, target_file in targets.iteritems():
            target_data = urllib2.urlopen(target_url).read()
            with open(target_file, 'w') as file_:
                file_.write(target_data)

        click.echo("pipeline was successfully archived")

    if command == 'notify':
        data = {}
        data['title'] = title
        data['message'] = message
        data['type'] = type
        data['links'] = {}
        for l in link:
            data['links'][l[0]] = {}
            data['links'][l[0]]['text'] = l[1]
            data['links'][l[0]]['url'] = l[2]

        click.echo("Sending data to %s:" % url)
        click.echo(json.dumps(data))

        req = urllib2.Request(url + "/pipeline/notify")
        req.add_header('Content-Type', 'application/json')
        urllib2.urlopen(req, json.dumps(data))

        click.echo("Notification successfull!")


if __name__ == '__main__':
    main()
