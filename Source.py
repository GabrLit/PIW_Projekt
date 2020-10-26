import cv2
import numpy as np


def diceRead(image):  # funkcja która przyjmuje jako wejście jedną z klatek z przechwyconego obrazu i zwraca obraz ze wszystkimi danymi rysowanymi
                      # tj. prostokątami lub kołami które oznaczają elementy jak i wartością sumaryczną kości.
    gray = rgb2gray(image)
    binary = binarization(gray, 0.5)

    cv2.imshow("Original", image)
    cv2.imshow("GrayScale", gray)
    cv2.imshow("Binary", binary)

    cv2.waitKey()
    cv2.destroyAllWindows()
    return  #zwracać ma obraz z rysowanymi elementami i wypisaną wartością.


def rgb2gray(image):
    B = image[:, :, 0]  #ekstrakcja każdego z kanałów -> openCV pracuje w formacie BGR nie RGB!!
    G = image[:, :, 1]
    R = image[:, :, 2]

    gray = (0.3 * R + 0.59 * G + 0.11 * B) #https://www.tutorialspoint.com/dip/grayscale_to_rgb_conversion.htm -> metoda ważona przetwarzania na grayscale
    gray = gray.astype(np.uint8) #konwersja do uint8

    return gray


def binarization(image, level): #jako parametr obraz grayscale i poziom binaryzacji (domyślnie przyjmujemy 0.5 czyli 50%)
    plevel = level * 255    #percentage level
    binary = image > plevel #numpy operator porównania-> zwraca macierz booleanów, True jeżeli warunek spełniony False jeżeli nie
    binary = binary * 255   #zera i jedynki(True False) z macierzy booleanów po pomnożeniu *255 dadzą 0 i 255-> czarny i biały
    binary = binary.astype(np.uint8) #konwersja typu

    return binary

image = cv2.imread("pictures/index.jpeg")
diceRead(image)
