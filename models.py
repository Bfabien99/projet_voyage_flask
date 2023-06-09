import sqlite3


class DbManager:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("voyage_commun.db")
        self.connection.row_factory = (
            sqlite3.Row
        )  # RETOURNER LES DONNÉES SOUS FORME DE DICTIONNAIRE
        self.cur = self.connection.cursor()

    # CREATION D'UNE TABLE DE MANIERE DYNAMIQUE
    # ASSEZ BASIQUE
    def create_table(self, table_name: str, params=()) -> bool:
        """
        Cette fonction permet de créer une table avec ses colonnes de manière dynamique

        Args:
            table_name (str): Le nom de la table dans la base de donnée
            params (tuple): Les différentes colonnes de la table

        Returns:
            bool: résultat
        """
        sql = f"CREATE TABLE IF NOT EXISTS {table_name}"
        sql += """(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            """
        for param in params:
            sql += f"{param} VARCHAR(200) NOT NULL,"
        sql = sql[:-1]  # ON SUPPRIME LA DERNIÈRE VIRGULE
        sql += ")"
        try:
            #print(sql)
            self.cur.execute(sql)
            return True
        except Exception as e:
            print(f"error: {e}")
            return False


class Voyage(DbManager):
    def __init__(
        self,
        id: str = "",
        ville_depart: str = "",
        ville_arrivee: str = "",
        date: str = "",
        heure: str = "",
    ) -> None:
        super().__init__()
        self.id = id
        self.ville_depart = ville_depart
        self.ville_arrivee = ville_arrivee
        self.date = date
        self.heure = heure
        self.create_table("voyages", ("ville_depart", "ville_arrivee", "date", "heure"))

    def get_all(self):
        try:
            voyages = self.cur.execute("SELECT * FROM voyages")
            return voyages.fetchall()
        except Exception as e:
            print(f"error: {e}")
            return False

    def get_by_id(self):
        try:
            voyage = self.cur.execute("SELECT * FROM voyages WHERE id=?", (self.id,))
            return voyage.fetchone()
        except Exception as e:
            print(f"error: {e}")
            return False

    def is_exist(self):
        try:
            voyages = self.cur.execute(
                "SELECT * FROM voyages WHERE ville_depart=? AND ville_arrivee=?", (self.ville_depart, self.ville_arrivee)
            )
            return voyages.fetchall()
        except Exception as e:
            print(f"error: {e}")
            return False
        
    def delete_by_id(self):
        try:
            self.cur.execute("DELETE FROM voyages WHERE id=?", (self.id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"error: {e}")
            return False

    def insert(self):
        sql = "INSERT INTO voyages(ville_depart, ville_arrivee, date, heure) VALUES(?,?,?,?)"
        try:
            self.cur.execute(
                sql, (self.ville_depart, self.ville_arrivee, self.date, self.heure)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"error: {e}")
            return False

    def update(self):
        sql = "UPDATE voyages SET ville_depart=? ville_arrivee=? date=? heure=? WHERE id=?"
        try:
            self.cur.execute(
                sql,
                (self.ville_depart, self.ville_arrivee, self.date, self.heure, self.id),
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"error: {e}")
            return False


class Ville(DbManager):
    def __init__(self, id: str = "", nom_ville: str = "") -> None:
        super().__init__()
        self.ville = nom_ville
        self.create_table("ville", ("nom_ville",))

    def get_all(self):
        try:
            ville = self.cur.execute("SELECT * FROM ville")
            return ville.fetchall()
        except Exception as e:
            print(f"error: {e}")
            return False

    def get_by_id(self):
        try:
            ville = self.cur.execute("SELECT * FROM ville WHERE id=?", (self.id,))
            return ville.fetchone()
        except Exception as e:
            print(f"error: {e}")
            return False

    def is_exist(self):
        try:
            ville = self.cur.execute(
                "SELECT * FROM ville WHERE nom_ville=?", (self.ville,)
            )
            if ville.fetchone():
                return True
        except Exception as e:
            print(f"error: {e}")
            return False

    def delete_by_id(self):
        try:
            self.cur.execute("DELETE FROM ville WHERE id=?", (self.id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"error: {e}")
            return False

    def insert(self):
        sql = "INSERT INTO ville(nom_ville) VALUES(?)"
        try:
            self.cur.execute(sql, (self.ville,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"error: {e}")
            return False

    def update(self):
        sql = "UPDATE ville SET nom_ville=? WHERE id=?"
        try:
            self.cur.execute(sql, (self.ville, self.id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"error: {e}")
            return False
