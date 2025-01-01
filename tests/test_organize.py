# create a test for the organize_files function
import os
import pathlib
import tempfile

from core.organizer import organize_files



def test_organize_files_move():
    # create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # create some test files with different modified dates
        file1 = os.path.join(tmpdirname, "file1.txt")
        with open(file1, "w") as f:
            f.write("test file 1")
        os.utime(file1, (0, 0))

        file2 = os.path.join(tmpdirname, "file2.txt")
        with open(file2, "w") as f:
            f.write("test file 2")
        os.utime(file2, (1000000000, 1000000000))

        file3 = os.path.join(tmpdirname, "file3.txt")
        with open(file3, "w") as f:
            f.write("test file 3")
        os.utime(file3, (2000000000, 2000000000))

        # call the organize_files function
        organize_files(pathlib.Path(tmpdirname), pathlib.Path(tmpdirname), "mv")

        # check if the files are organized correctly
        assert pathlib.Path(tmpdirname, "1970", "01January1970", "file1.txt").exists()
        assert pathlib.Path(tmpdirname, "2001", "09September2001", "file2.txt").exists()
        assert pathlib.Path(tmpdirname, "2033", "05May2033", "file3.txt").exists()

        # check if the original files are gone
        assert not pathlib.Path(tmpdirname, "file1.txt").exists()
        assert not pathlib.Path(tmpdirname, "file2.txt").exists()
        assert not pathlib.Path(tmpdirname, "file3.txt").exists()


def test_organize_files_copy():
    # create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # create some test files with different modified dates
        file1 = os.path.join(tmpdirname, "file1.txt")
        with open(file1, "w") as f:
            f.write("test file 1")
        os.utime(file1, (0, 0))

        file2 = os.path.join(tmpdirname, "file2.txt")
        with open(file2, "w") as f:
            f.write("test file 2")
        os.utime(file2, (1000000000, 1000000000))

        file3 = os.path.join(tmpdirname, "file3.txt")
        with open(file3, "w") as f:
            f.write("test file 3")
        os.utime(file3, (2000000000, 2000000000))

        # call the organize_files function
        organize_files(pathlib.Path(tmpdirname), pathlib.Path(tmpdirname), "cp")

        # check if the files are organized correctly
        assert pathlib.Path(tmpdirname, "1970", "01January1970", "file1.txt").exists()
        assert pathlib.Path(tmpdirname, "2001", "09September2001", "file2.txt").exists()
        assert pathlib.Path(tmpdirname, "2033", "05May2033", "file3.txt").exists()

        # check if the original files are still there
        assert pathlib.Path(tmpdirname, "file1.txt").exists()
        assert pathlib.Path(tmpdirname, "file2.txt").exists()
        assert pathlib.Path(tmpdirname, "file3.txt").exists()


def test_organize_file_another_destination_move():
    # create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # create some test files with different modified dates
        file1 = os.path.join(tmpdirname, "file1.txt")
        with open(file1, "w") as f:
            f.write("test file 1")
        os.utime(file1, (0, 0))

        file2 = os.path.join(tmpdirname, "file2.txt")
        with open(file2, "w") as f:
            f.write("test file 2")
        os.utime(file2, (1000000000, 1000000000))

        file3 = os.path.join(tmpdirname, "file3.txt")
        with open(file3, "w") as f:
            f.write("test file 3")
        os.utime(file3, (2000000000, 2000000000))

        # create a temporary destination directory
        with tempfile.TemporaryDirectory() as tmpdirname_dest:
            # call the organize_files function
            organize_files(pathlib.Path(tmpdirname), pathlib.Path(tmpdirname_dest), "mv")

            # check if the files are organized correctly
            assert pathlib.Path(tmpdirname_dest, "1970", "01January1970", "file1.txt").exists()
            assert pathlib.Path(tmpdirname_dest, "2001", "09September2001", "file2.txt").exists()
            assert pathlib.Path(tmpdirname_dest, "2033", "05May2033", "file3.txt").exists()

        # check if the original files are gone
        assert not pathlib.Path(tmpdirname, "file1.txt").exists()
        assert not pathlib.Path(tmpdirname, "file2.txt").exists()
        assert not pathlib.Path(tmpdirname, "file3.txt").exists()


def test_organize_file_another_destination_copy():
    # create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # create some test files with different modified dates
        file1 = os.path.join(tmpdirname, "file1.txt")
        with open(file1, "w") as f:
            f.write("test file 1")
        os.utime(file1, (0, 0))

        file2 = os.path.join(tmpdirname, "file2.txt")
        with open(file2, "w") as f:
            f.write("test file 2")
        os.utime(file2, (1000000000, 1000000000))

        file3 = os.path.join(tmpdirname, "file3.txt")
        with open(file3, "w") as f:
            f.write("test file 3")
        os.utime(file3, (2000000000, 2000000000))

        # create a temporary destination directory
        with tempfile.TemporaryDirectory() as tmpdirname_dest:
            # call the organize_files function
            organize_files(pathlib.Path(tmpdirname), pathlib.Path(tmpdirname_dest), "cp")

            # check if the files are organized correctly
            assert pathlib.Path(tmpdirname_dest, "1970", "01January1970", "file1.txt").exists()
            assert pathlib.Path(tmpdirname_dest, "2001", "09September2001", "file2.txt").exists()
            assert pathlib.Path(tmpdirname_dest, "2033", "05May2033", "file3.txt").exists()

        # check if the original files are still there
        assert pathlib.Path(tmpdirname, "file1.txt").exists()
        assert pathlib.Path(tmpdirname, "file2.txt").exists()
        assert pathlib.Path(tmpdirname, "file3.txt").exists()