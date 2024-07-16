from db._database import _Database
from board.scripts import app, update_layout

if __name__ == '__main__':
    db = _Database('Project 1', ['rmse', 'mae'])
    update_layout(db.select_experiments_data(), 'Project 1')
    app.run_server(debug=True)
