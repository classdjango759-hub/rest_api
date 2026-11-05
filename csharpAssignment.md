# OOP Assignment: Vehicle Fleet Management

**Language:** C# (console app)
**Builds on:** The 4 OOP pillars you taught
**Time:** 1 week

---

## What You're Building

A console application that manages a fleet of vehicles for a delivery company. The user can:
- Add vehicles (different types)
- List all vehicles
- Show each vehicle's details (looks different based on type)
- Calculate fuel cost for a trip (each type burns fuel differently)
- Calculate annual maintenance cost (each type costs differently)

The whole point: you'll use **all 4 OOP pillars** and it will be obvious *why* each one is there.

---

## The 4 Pillars — Where They Show Up

| Pillar | Where it appears |
|--------|-----------------|
| **Encapsulation** | Every class has private fields. You access them through properties with validation (e.g., fuel tank size can't be negative). |
| **Abstraction** | The base `Vehicle` class is `abstract`. It defines *what* every vehicle must do, but not *how*. You can't create a plain `Vehicle` — only a `Car`, `Truck`, or `Motorcycle`. |
| **Inheritance** | `Car`, `Truck`, and `Motorcycle` all inherit from `Vehicle`. They get the shared fields (plate number, fuel tank, mileage) for free. |
| **Polymorphism** | Every vehicle has a `CalculateFuelCost()` and `CalculateMaintenance()` method, but each type calculates them differently. You call `vehicle.CalculateFuelCost(500)` and the right version runs automatically. |

---

## Your Class Structure

```
Vehicle (abstract)
├── Car
├── Truck
└── Motorcycle
```

### Base Class: `Vehicle` (abstract)

| Member | Type | Notes |
|--------|------|-------|
| `_plateNumber` | `string` (private) | Must not be null or empty. Must be 7 characters. |
| `_brand` | `string` (private) | Like "Toyota", "Ford". Must not be empty. |
| `_modelYear` | `int` (private) | Must be between 1990 and 2026. |
| `_fuelTankSize` | `decimal` (private) | In liters. Must be > 0. |
| `_fuelEfficiency` | `decimal` (private) | Km per liter. Must be > 0. |
| `_mileage` | `decimal` (private) | Total km driven. Must be ≥ 0. |
| `PlateNumber` | `string` (property) | Get + Set with validation. |
| `Brand` | `string` (property) | Get + Set. |
| `ModelYear` | `int` (property) | Get + Set with range check. |
| `FuelTankSize` | `decimal` (property) | Get + Set (must be > 0). |
| `FuelEfficiency` | `decimal` (property) | Get + Set (must be > 0). |
| `Mileage` | `decimal` (property) | Get + Set (must be ≥ 0). |
| `CalculateFuelCost(decimal distanceKm)` | `abstract decimal` | Each subclass must implement this. |
| `CalculateMaintenance()` | `abstract decimal` | Annual maintenance. Each subclass must implement this. |
| `DisplayInfo()` | `virtual string` | Returns a formatted string. Subclasses override to add extra info. |

**What the you writes for this class:**
- Private fields
- Properties with get/set and validation in the setter
- A constructor that takes the 6 shared parameters
- `CalculateFuelCost()` declared as `abstract`
- `CalculateMaintenance()` declared as `abstract`
- `DisplayInfo()` declared as `virtual` with a basic implementation (shows plate, brand, year, mileage)

---

### Derived Class: `Car`

A car is used for short deliveries. Its fuel cost is straightforward: distance ÷ efficiency × fuel price. Maintenance is a flat $400/year plus $0.05 per km driven.

| Extra Member | Type | Notes |
|-------------|------|-------|
| `_seats` | `int` (private) | Must be 2–7. |
| `_hasAirConditioning` | `bool` (private) | If true, fuel efficiency drops by 10%. |
| `Seats` | `int` (property) | Get + Set with validation. |
| `HasAirConditioning` | `bool` (property) | Get + Set. |
| `CalculateFuelCost(decimal distanceKm)` | `decimal` (override) | If AC is on: use `FuelEfficiency * 0.9`. Then: `distance / efficiency * 1.55m` (fuel price per liter). |
| `CalculateMaintenance()` | `decimal` (override) | `400m + (Mileage * 0.05m)` |
| `DisplayInfo()` | `string` (override) | Calls `base.DisplayInfo()` then appends seats and AC status. |

---

### Derived Class: `Truck`

A truck is used for heavy deliveries. It has a cargo capacity. Its fuel cost depends on whether it's loaded or empty (loaded = 30% worse efficiency). Maintenance is based on cargo weight: $0.02 per kg of capacity, plus $0.03 per km driven.

| Extra Member | Type | Notes |
|-------------|------|-------|
| `_cargoCapacity` | `decimal` (private) | In kg. Must be > 0. |
| `_currentLoad` | `decimal` (private) | In kg. Must be ≥ 0 and ≤ cargoCapacity. |
| `CargoCapacity` | `decimal` (property) | Get + Set (must be > 0). |
| `CurrentLoad` | `decimal` (property) | Get + Set (must be ≥ 0 and ≤ CargoCapacity). |
| `CalculateFuelCost(decimal distanceKm)` | `decimal` (override) | If `CurrentLoad > 0`: efficiency drops by 30%. Then: `distance / effectiveEfficiency * 1.55m`. |
| `CalculateMaintenance()` | `decimal` (override) | `(CargoCapacity * 0.02m) + (Mileage * 0.03m)` |
| `DisplayInfo()` | `string` (override) | Calls `base.DisplayInfo()` then appends cargo capacity and current load. |

---

### Derived Class: `Motorcycle`

A motorcycle is used for quick urban deliveries. It's cheap to fuel but has higher maintenance per km (more wear and tear). Fuel cost: distance ÷ efficiency × fuel price. Maintenance: $200/year + $0.08 per km (higher than a car because of the single wheel).

| Extra Member | Type | Notes |
|-------------|------|-------|
| `_engineSize` | `int` (private) | In cc (cubic centimeters). Must be 50–1000. |
| `_hasTopBox` | `bool` (private) | A storage box on the back. If true, efficiency drops by 5%. |
| `EngineSize` | `int` (property) | Get + Set with range check. |
| `HasTopBox` | `bool` (property) | Get + Set. |
| `CalculateFuelCost(decimal distanceKm)` | `decimal` (override) | If top box is on: use `FuelEfficiency * 0.95`. Then: `distance / effectiveEfficiency * 1.55m`. |
| `CalculateMaintenance()` | `decimal` (override) | `200m + (Mileage * 0.08m)` |
| `DisplayInfo()` | `string` (override) | Calls `base.DisplayInfo()` then appends engine size and top box status. |

---

## The Main Program (What You Builds in `Program.cs`)

A simple menu-driven console app:

```
=== Vehicle Fleet Manager ===
1. Add a Car
2. Add a Truck
3. Add a Motorcycle
4. List all vehicles
5. Calculate trip cost (all vehicles, 500 km)
6. Annual maintenance report
7. Exit

Choose: 
```

**What each option does:**

| Option | What happens |
|--------|-------------|
| 1 | Ask for plate, brand, year, tank size, fuel efficiency, mileage, seats, AC (y/n). Create a `Car`. Add to list. |
| 2 | Ask for plate, brand, year, tank size, fuel efficiency, mileage, cargo capacity, current load. Create a `Truck`. Add to list. |
| 3 | Ask for plate, brand, year, tank size, fuel efficiency, mileage, engine size, top box (y/n). Create a `Motorcycle`. Add to list. |
| 4 | Loop through the list. Call `DisplayInfo()` on each one. Print the result. |
| 5 | Ask for a distance. Loop through the list. Call `CalculateFuelCost(distance)` on each one. Print name, type, and cost. At the bottom, print the total. |
| 6 | Loop through the list. Call `CalculateMaintenance()` on each one. Print name, type, and cost. At the bottom, print the total. |
| 7 | `Environment.Exit(0)` |

**Key point:** In options 4, 5, and 6, you loop through a `List<Vehicle>` (the base type). You call methods on the base type, but the **correct version** runs for each object. That's polymorphism in action.

 ## Example

```csharp
List<Vehicle> fleet = new List<Vehicle>();

// Adding:
fleet.Add(new Car("ABC-1234", "Toyota", 2023, 50m, 12m, 15000m, 5, true));
fleet.Add(new Truck("XYZ-5678", "Ford", 2021, 200m, 5m, 80000m, 3000m, 2500m));
fleet.Add(new Motorcycle("MNO-9012", "Yamaha", 2024, 15m, 25m, 8000m, 250, false));

// Listing (polymorphism — the right DisplayInfo runs for each):
foreach (Vehicle v in fleet)
{
    Console.WriteLine(v.DisplayInfo());
}

// Trip cost (polymorphism — the right CalculateFuelCost runs for each):
decimal distance = 500m;
decimal total = 0;
foreach (Vehicle v in fleet)
{
    decimal cost = v.CalculateFuelCost(distance);
    total += cost;
    Console.WriteLine($"{v.PlateNumber}: ${cost:F2}");
}
Console.WriteLine($"Total fuel cost for {distance} km: ${total:F2}");
```

---

## What You Must Deliver

| # | What | Why |
|---|------|-----|
| 1 | `Vehicle.cs` — abstract base class | Tests: encapsulation, abstraction |
| 2 | `Car.cs` | Tests: inheritance, polymorphism, conditional logic (AC) |
| 3 | `Truck.cs` | Tests: inheritance, polymorphism, load-dependent calculation |
| 4 | `Motorcycle.cs` | Tests: inheritance, polymorphism, conditional logic (top box) |
| 5 | `Program.cs` — the menu-driven app | Tests: they can wire it all together |
| 6 | A screenshot or recording of the app running (adding all 3 types, listing, showing trip cost and maintenance) | Proof it works |

---

## Grading Rubric (100 points)

| What I'm checking | Points |
|-------------------|--------|
| `Vehicle` is `abstract` with private fields and validated properties | 15 |
| All 3 derived classes inherit correctly and add their own fields with validation | 20 |
| `CalculateFuelCost()` is `abstract` in the base and `override` in all 3 — and each calculates differently | 20 |
| `CalculateMaintenance()` is `abstract` in the base and `override` in all 3 — and each uses a different formula | 10 |
| `DisplayInfo()` uses `virtual`/`override` and calls `base.DisplayInfo()` | 10 |
| The main program uses a `List<Vehicle>` and calls methods through the base type (polymorphism) | 15 |
| Validation works (try setting a negative tank size or a load bigger than capacity — it should reject it) | 10 |
| Code is clean: proper naming, no magic numbers, comments where needed | 10 |

---

## Common Mistakes to Warn Students About

| Mistake | Why it's wrong |
|---------|---------------|
| Making `Vehicle` not abstract | Then they can do `new Vehicle(...)` which doesn't make sense. |
| Forgetting `override` keyword | The method won't actually replace the base one. You'll get a compile error or the wrong behavior. |
| Not calling `base.DisplayInfo()` | They lose the plate, brand, year, and mileage in the output. |
| Using `double` for money | Use `decimal`. Money is never a float or double. |
| Putting `_fuelEfficiency` in each derived class instead of the base | That's what inheritance is for. Don't repeat yourself. |
| Making the list `List<Car>` instead of `List<Vehicle>` | Then you lose polymorphism. You need one list that holds all types. |
| Forgetting the conditional (AC, load, top box) | The whole point of each subclass is that it calculates *differently*. If it's the same formula, you don't need a separate class. |

---

## Stretch Goal (Bonus 10 points)

Add an 8th option to the menu: **"Add mileage"**. Ask for a plate number and a distance. Find the vehicle in the list, add the distance to its `Mileage`, and confirm.

Then add a 9th option: **"Refuel"**. Ask for a plate number. Show how much fuel is in the tank (assume it starts empty) and fill it to full. Print the cost: `FuelTankSize * 1.55m`.

This teaches you:
- `List<T>.Find()` or LINQ's `.FirstOrDefault()` to search by plate
- The `is` keyword: `if (vehicle is Truck t)` → "Loaded truck — fuel cost will be higher."

---

## Suggested File Layout

```
FleetManager/
├── FleetManager.csproj
├── Program.cs
├── Models/
│   ├── Vehicle.cs
│   ├── Car.cs
│   ├── Truck.cs
│   └── Motorcycle.cs
└── README.md
```

---

> "You already know what an abstract class is. Now build a fleet manager. Three types of vehicles, each one burns fuel differently and costs a different amount to maintain. But in your list, they're all just `Vehicle`. You call the same method on each one and get a different answer. That's the whole point of OOP."

