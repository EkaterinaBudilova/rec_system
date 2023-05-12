import pandas as pd

class RecSys:
    def __init__(self, basematrix_name: str, filename: str) -> None:
        self.cross_factor = basematrix_name
        self.datafile = filename

    @property
    def cross_factor(self):
        return self.__cross_factor
    
    @cross_factor.setter
    def cross_factor(self, basematrix_name: str) -> None:
        base = pd.read_csv(basematrix_name)
        cf = base.pivot_table(index='UID', columns='JID', values='Rating').fillna(0)
        self.__cross_factor = cf

    @property
    def datafile(self):
        return self.__datafile
    
    @datafile.setter
    def datafile(self, filename: str):
        input_data = pd.read_csv(filename, names=['UID'], sep=";")
        self.__datafile = input_data

    def _get_users_predictions(self, user_id: int, n: int, model):
        rec_items = pd.DataFrame(model.loc[user_id])
        rec_items.columns = ['predicted_rating']
        rec_items = rec_items.sort_values('predicted_rating', ascending=False)
        rec_items = rec_items.head(n)
        first_rec = rec_items.head(1)
        first_rating = rec_items.head(1).predicted_rating
        return list(({first_rec.index[0]: first_rating.item()}, rec_items.index.tolist()))

    def get_result(self, path):
        self.datafile['result'] = self.datafile['UID'].apply(lambda x: self._get_users_predictions(x, 10, self.cross_factor))
        self.datafile.result.tolist()
        self.datafile.to_csv(path, sep=';', index=False)
       



    
