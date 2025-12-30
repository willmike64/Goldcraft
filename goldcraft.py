#!/usr/bin/env python3
"""
Goldcraft - A Star System Exploration Game

Navigate through a star system, mine resources from planets,
and build your fortune!
"""

import random
import sys
from typing import Dict, List, Tuple


class Planet:
    """Represents a planet in the star system."""
    
    def __init__(self, name: str, distance: float, resources: Dict[str, int]):
        self.name = name
        self.distance = distance  # Distance from star in AU
        self.resources = resources
        self.discovered = False
    
    def __str__(self):
        resource_str = ", ".join([f"{k}: {v}" for k, v in self.resources.items()])
        return f"{self.name} (Distance: {self.distance} AU) - Resources: {resource_str}"


class Ship:
    """Represents the player's ship."""
    
    MAX_FUEL = 100
    
    def __init__(self):
        self.fuel = self.MAX_FUEL
        self.cargo_capacity = 50
        self.cargo: Dict[str, int] = {"gold": 0, "iron": 0, "crystals": 0}
        self.credits = 100
    
    def get_cargo_used(self) -> int:
        return sum(self.cargo.values())
    
    def get_cargo_space(self) -> int:
        return self.cargo_capacity - self.get_cargo_used()
    
    def add_resource(self, resource: str, amount: int) -> int:
        """Add resource to cargo. Returns amount actually added."""
        space = self.get_cargo_space()
        actual_amount = min(amount, space)
        if resource in self.cargo:
            self.cargo[resource] += actual_amount
        else:
            self.cargo[resource] = actual_amount
        return actual_amount
    
    def __str__(self):
        cargo_str = ", ".join([f"{k}: {v}" for k, v in self.cargo.items()])
        return f"Ship Status:\n  Fuel: {self.fuel}\n  Credits: {self.credits}\n  Cargo ({self.get_cargo_used()}/{self.cargo_capacity}): {cargo_str}"


class StarSystem:
    """Represents the star system with planets."""
    
    def __init__(self):
        self.planets: List[Planet] = []
        self.generate_system()
        self.current_planet_index = 0
        self.planets[0].discovered = True
    
    def generate_system(self):
        """Generate a random star system with planets."""
        planet_names = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
        
        for i, name in enumerate(planet_names):
            distance = (i + 1) * 1.5
            resources = {
                "gold": random.randint(10, 100),
                "iron": random.randint(20, 150),
                "crystals": random.randint(5, 50)
            }
            self.planets.append(Planet(name, distance, resources))
    
    def get_current_planet(self) -> Planet:
        return self.planets[self.current_planet_index]
    
    def travel_to_planet(self, planet_index: int, ship: Ship) -> Tuple[bool, str]:
        """Travel to a planet. Returns (success, message)."""
        if planet_index < 0 or planet_index >= len(self.planets):
            return False, "Invalid planet index!"
        
        current = self.planets[self.current_planet_index]
        target = self.planets[planet_index]
        
        fuel_cost = int(abs(target.distance - current.distance) * 5)
        
        if ship.fuel < fuel_cost:
            return False, f"Not enough fuel! Need {fuel_cost}, have {ship.fuel}"
        
        ship.fuel -= fuel_cost
        self.current_planet_index = planet_index
        target.discovered = True
        
        return True, f"Traveled to {target.name}. Fuel used: {fuel_cost}"


class Game:
    """Main game controller."""
    
    def __init__(self):
        self.ship = Ship()
        self.star_system = StarSystem()
        self.running = True
        self.turn = 1
    
    def display_menu(self):
        """Display the main game menu."""
        print("\n" + "=" * 50)
        print(f"GOLDCRAFT - Turn {self.turn}")
        print("=" * 50)
        print(f"\nCurrent Location: {self.star_system.get_current_planet().name}")
        print(self.ship)
        print("\nActions:")
        print("  1. Mine resources")
        print("  2. Travel to another planet")
        print("  3. View star system")
        print("  4. Trade at station")
        print("  5. Refuel ship")
        print("  6. Quit game")
        print()
    
    def mine_resources(self):
        """Mine resources from current planet."""
        planet = self.star_system.get_current_planet()
        
        if self.ship.fuel < 10:
            print("Not enough fuel to mine! (Need 10 fuel)")
            return
        
        print(f"\nMining on {planet.name}...")
        
        # Mine random amounts
        mined: Dict[str, int] = {}
        for resource, available in planet.resources.items():
            if available > 0:
                amount = random.randint(1, min(10, available))
                actual = self.ship.add_resource(resource, amount)
                if actual > 0:
                    mined[resource] = actual
                    planet.resources[resource] -= actual
        
        self.ship.fuel -= 10
        
        if mined:
            print("Mined:")
            for resource, amount in mined.items():
                print(f"  {resource}: {amount}")
        else:
            print("No resources mined (cargo full or planet depleted)")
    
    def travel(self):
        """Handle travel to another planet."""
        print("\nAvailable Planets:")
        for i, planet in enumerate(self.star_system.planets):
            if planet.discovered:
                current = " <- Current" if i == self.star_system.current_planet_index else ""
                print(f"  {i + 1}. {planet}{current}")
            else:
                print(f"  {i + 1}. Unknown Planet (Distance: {planet.distance} AU)")
        
        try:
            choice = input("\nSelect planet number (or 0 to cancel): ")
            planet_num = int(choice)
            
            if planet_num == 0:
                return
            
            planet_index = planet_num - 1
            success, message = self.star_system.travel_to_planet(planet_index, self.ship)
            print(f"\n{message}")
            
        except ValueError:
            print("Invalid input!")
    
    def view_system(self):
        """Display information about the star system."""
        print("\nStar System Map:")
        print("-" * 50)
        for i, planet in enumerate(self.star_system.planets):
            current = " <- Current" if i == self.star_system.current_planet_index else ""
            if planet.discovered:
                print(f"  {i + 1}. {planet}{current}")
            else:
                print(f"  {i + 1}. ???{current}")
    
    def trade(self):
        """Trade resources for credits."""
        print("\nTrading Station:")
        print("Prices:")
        prices = {"gold": 10, "iron": 5, "crystals": 15}
        
        total_value = sum(self.ship.cargo[r] * prices.get(r, 0) for r in self.ship.cargo)
        
        if total_value == 0:
            print("You have nothing to trade!")
            return
        
        for resource, amount in self.ship.cargo.items():
            if amount > 0:
                price = prices.get(resource, 0)
                print(f"  {resource}: {amount} units x {price} credits = {amount * price} credits")
        
        choice = input(f"\nSell all cargo for {total_value} credits? (y/n): ")
        
        if choice.lower() == 'y':
            self.ship.credits += total_value
            for resource in self.ship.cargo:
                self.ship.cargo[resource] = 0
            print(f"\nSold all cargo for {total_value} credits!")
            print(f"Total credits: {self.ship.credits}")
    
    def refuel(self):
        """Refuel the ship."""
        fuel_price = 1  # 1 credit per fuel unit
        needed_fuel = Ship.MAX_FUEL - self.ship.fuel
        
        if needed_fuel == 0:
            print("\nFuel tank is already full!")
            return
        
        cost = needed_fuel * fuel_price
        
        if self.ship.credits < cost:
            # Partial refuel
            affordable = self.ship.credits // fuel_price
            if affordable == 0:
                print("\nNot enough credits to refuel!")
                return
            
            print(f"\nCan afford {affordable} fuel units for {affordable} credits")
            choice = input("Refuel? (y/n): ")
            
            if choice.lower() == 'y':
                self.ship.fuel += affordable
                self.ship.credits -= affordable
                print(f"Refueled {affordable} units. Current fuel: {self.ship.fuel}")
        else:
            print(f"\nFull refuel costs {cost} credits")
            choice = input("Refuel to full? (y/n): ")
            
            if choice.lower() == 'y':
                self.ship.fuel = Ship.MAX_FUEL
                self.ship.credits -= cost
                print(f"Refueled to full. Current fuel: {self.ship.fuel}")
    
    def check_game_over(self) -> bool:
        """Check if game over conditions are met."""
        if self.ship.fuel == 0 and self.ship.credits < 1:
            print("\n" + "=" * 50)
            print("GAME OVER!")
            print("You've run out of fuel and credits!")
            print(f"Final Score: {sum(self.ship.cargo.values()) * 10} points")
            print("=" * 50)
            return True
        return False
    
    def run(self):
        """Main game loop."""
        print("\n" + "=" * 50)
        print("Welcome to GOLDCRAFT!")
        print("=" * 50)
        print("\nYou are a space miner exploring a star system.")
        print("Mine resources, trade them for credits, and explore new planets!")
        print("\nObjective: Collect as much gold and resources as you can!")
        
        while self.running:
            if self.check_game_over():
                break
            
            self.display_menu()
            
            choice = input("Choose an action: ")
            
            if choice == "1":
                self.mine_resources()
            elif choice == "2":
                self.travel()
            elif choice == "3":
                self.view_system()
            elif choice == "4":
                self.trade()
            elif choice == "5":
                self.refuel()
            elif choice == "6":
                print("\nThanks for playing Goldcraft!")
                print(f"Final Credits: {self.ship.credits}")
                print(f"Resources Collected: {sum(self.ship.cargo.values())} units")
                self.running = False
            else:
                print("Invalid choice!")
            
            self.turn += 1
        
        print("\nGame ended!")


def main():
    """Entry point for the game."""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)


if __name__ == "__main__":
    main()
