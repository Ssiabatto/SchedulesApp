from odoo import api, fields, models

class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = None
        self.models = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with the Odoo API and set up the models."""
        self.common = models.Model(self.url, self.db, self.username, self.password)
        self.models = api.Model(self.url, self.db, self.username, self.password)

    def create_record(self, model_name, values):
        """Create a new record in the specified model."""
        return self.models.execute_kw(model_name, 'create', [values])

    def read_record(self, model_name, record_id):
        """Read a record from the specified model."""
        return self.models.execute_kw(model_name, 'read', [[record_id]])

    def update_record(self, model_name, record_id, values):
        """Update an existing record in the specified model."""
        return self.models.execute_kw(model_name, 'write', [[record_id], values])

    def delete_record(self, model_name, record_id):
        """Delete a record from the specified model."""
        return self.models.execute_kw(model_name, 'unlink', [[record_id]])

    def search_records(self, model_name, domain):
        """Search for records in the specified model based on a domain."""
        return self.models.execute_kw(model_name, 'search', [domain])