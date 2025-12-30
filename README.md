# Goldcraft

A text-based star system exploration and resource mining game. Navigate through planets, mine valuable resources like gold and crystals, trade for credits, and build your fortune!

## About

This is a game based on classic star system exploration games. Pilot your ship through a solar system, discover new planets, mine resources, and manage your fuel and cargo as you build your mining empire.

## Features

- **Explore a Star System**: Travel between 8 different planets, each with unique resources
- **Resource Mining**: Mine gold, iron, and crystals from planets
- **Resource Management**: Manage your ship's cargo capacity and fuel
- **Trading System**: Sell your resources at trading stations for credits
- **Strategic Gameplay**: Balance exploration, mining, and fuel management

## How to Play

### Installation

No installation required! Just make sure you have Python 3.6 or later installed.

### Running the Game

```bash
python3 goldcraft.py
```

Or make it executable and run directly:

```bash
chmod +x goldcraft.py
./goldcraft.py
```

### Game Controls

When playing, you'll have these options:

1. **Mine Resources**: Extract resources from your current planet (costs 10 fuel)
2. **Travel to Another Planet**: Move to a different planet (fuel cost based on distance)
3. **View Star System**: See the map of all discovered planets
4. **Trade at Station**: Sell your resources for credits
5. **Refuel Ship**: Buy fuel using your credits (1 credit per fuel unit)
6. **Quit Game**: Exit the game

### Gameplay Tips

- Start by mining resources on your starting planet
- Trade resources for credits to buy fuel
- Explore nearby planets first to conserve fuel
- Keep an eye on your fuel levels - running out with no credits means game over!
- Different planets have different amounts of resources
- Gold and crystals are worth more than iron when trading

### Resource Values

- **Gold**: 10 credits per unit
- **Iron**: 5 credits per unit  
- **Crystals**: 15 credits per unit

## Game Mechanics

- **Fuel**: Your ship starts with 100 fuel. Mining costs 10 fuel, and travel costs vary by distance
- **Cargo**: You can carry up to 50 units of resources
- **Credits**: Used to buy fuel. Start with 100 credits
- **Planets**: Each planet has different amounts of gold, iron, and crystals
- **Travel Cost**: Distance between planets × 5 fuel units

## Objective

Mine as many resources as possible, trade strategically, and explore the entire star system before running out of fuel and credits!

## Requirements

- Python 3.6 or later

## License

Open source - feel free to modify and share!
