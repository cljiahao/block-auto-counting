from db.base import Base
from db.session import engine
from components.splash import Splash
from pages.Main import Main


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    root = Splash(Main)
    root.mainloop()
