import ifcopenshell

def main():
    model_path = "samples/test.ifc"

    print("Opening IFC model...")
    model = ifcopenshell.open(model_path)

    print("Model opened successfully")

    elements = model.by_type("IfcProduct")

    print(f"Total IfcProduct elements: {len(elements)}")

    print("\nFirst 10 elements")

    for element in elements:
        guid = element.GlobalId
        name = element.Name
        ifc_class = element.is_a()

        print(f"{ifc_class} | {guid} | {name}")
     
if __name__ == "__main__":
    main()