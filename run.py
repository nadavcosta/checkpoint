from cTopics import Topics
from cScraper import Scraper


def run_year(year):
    """@[modeling a single year, month-by-month independently]

    :param year:
    :return:
    """

    topics_ = Topics(file='./data/titles_' + year + '.pickle')

    for m_index, m_text in topics_.data.items():  # (month_index / month_text)
        topics_.fit_transform(data=m_text)
        print('\n', "YEAR: ", year, " MONTH: ", m_index)
        topics_.print_n_dominante_words_topic_(n=15)


if __name__ == '__main__':
    year_to_model = '2019'

    run_year(year=year_to_model)

