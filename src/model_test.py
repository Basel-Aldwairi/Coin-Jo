import coin_model

model = coin_model.CoinModel()

message = ''
while True:

    if message == 'quit':
        break

    message = input('Enter File Path or Quit : ')
    img_path = message

    x, y = model.predict_image(img_path)

    print(f'predicted that the coin is {x} with {y * 100:.2f}% certainty')
