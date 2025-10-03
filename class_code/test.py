# import asyncio
# import code

# async def print_with_delay(message: str, delay: float) -> None:
#     """Prints a message after a specified delay."""
#     print(f"Starting: {message}")
#     await asyncio.sleep(delay)  # Non-blocking sleep
#     print(f"Finished: {message}")

# async def main():
#     # Create multiple tasks that will run concurrently
#     print("Starting main function...")

#     # Create three tasks with different delays
#     task1 = asyncio.create_task(print_with_delay("Task 1", 2))
#     task2 = asyncio.create_task(print_with_delay("Task 2", 1))
#     task3 = asyncio.create_task(print_with_delay("Task 3", 3))
#     code.interact(local=locals())

#     # Wait for all tasks to complete
#     await asyncio.gather(task1, task2, task3)

#     print("All tasks completed!")

# # Run the async program
# if __name__ == "__main__":
#     asyncio.run(main())


# try:
#     x = 10 / 0  # This will cause a ZeroDivisionError
# except ZeroDivisionError:
#     print("Cannot divide by zero!")
# finally:
#     print("This always runs.")

import asyncio

async def risky_operation(task_id: int, delay: float) -> None:
    """A function that might raise an error"""
    try:
        print(f"Task {task_id}: Starting risky operation")
        await asyncio.sleep(delay)

        # Simulate an error in task 2
        if task_id == 2:
            print(f"Task {task_id}: failed")
            raise ValueError(f"Task {task_id} failed!")

        print(f"Task {task_id}: Operation completed successfully")

    finally:
        # This will always run, even if there's an error
        print(f"Task {task_id}: Cleanup completed")

async def main():
    try:
        print("Starting main function...")

        # Create three tasks with different delays
        tasks = [
            asyncio.create_task(risky_operation(1, 2)),
            asyncio.create_task(risky_operation(2, 1)),  # This one will fail
            asyncio.create_task(risky_operation(3, 3))
        ]

        # Wait for all tasks to complete or fail
        await asyncio.gather(*tasks, return_exceptions=True)

    finally:
        print("Main function cleanup - Always executes!")

if __name__ == "__main__":
    asyncio.run(main())
