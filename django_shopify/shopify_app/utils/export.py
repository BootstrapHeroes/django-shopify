import csv


class Exporter(object):

    def csv(self, response, content):

        writer = csv.writer(response)
        for row in content:
            writer.writerow([value.encode("utf-8") for value in row])

        return response

    def export(self, format, response, content):

        return getattr(self, format)(response, content)