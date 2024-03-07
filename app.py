from model.large_files_finder_model import LargeFilesFinderModel
from view.large_files_finder_view import LargeFilesFinderView
from presenter.large_file_finder_presenter import LargeFilesFinderPresenter


def main():
    model = LargeFilesFinderModel()
    presenter = LargeFilesFinderPresenter(None, model)
    view = LargeFilesFinderView(presenter)
    presenter.view = view
    view.mainloop()


if __name__ == "__main__":
    main()
