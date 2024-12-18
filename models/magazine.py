from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be of type int")
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._name = name
        else:
            raise TypeError("name must be of type str and between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category) > 0:
            self._category = category
        else:
            raise TypeError("category must be of type str and longer than zero characters")

    @property
    def articles(self):
        """
        Property method to retrieve the articles of the magazine.
        """
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles 
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        article_info = cursor.fetchall()
        conn.close()
        if article_info:
            return [Article(article["id"], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in article_info]
        else:
            return []

    @property
    def contributors(self):
        """
        Property method to retrieve the contributors of the magazine.
        """
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = '''
            SELECT DISTINCT authors.id, authors.name
            FROM authors 
            JOIN articles  ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        '''
        cursor.execute(sql, (self.id,))
        author_info = cursor.fetchall()
        conn.close()
        if author_info:
            return [Author(author["id"], author['name']) for author in author_info]
        else:
            return []

    def article_titles(self):
        return [article.title for article in self.articles]

    def contributing_authors(self):
        if self.contributors:
            contributing = [contributor for contributor in self.contributors if len([article for article in self.articles if article.author.id == contributor.id]) > 2]
            return contributing
        else:
            return None

    def __repr__(self):
        contributer_titles = "; ".join([contributer.name for contributer in self.contributors]) if self.contributors else "None"
        major_contributors = ";".join([contributer.name for contributer in self.contributing_authors()]) if self.contributing_authors() else "None"
        article_titles = ";".join([article.title for article in self.articles]) if self.articles else "None"
        return f'MAGAZINE:{self.name} ||ID: {self.id} || ARTIC:{article_titles}|| CONTR:{contributer_titles} || MAJOR CONTR:{major_contributors}'