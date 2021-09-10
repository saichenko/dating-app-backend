from invoke import task

##############################################################################
# Data generation for database
##############################################################################


@task
def fill_sample_data(context):
    """Prepare sample data for local usage."""
    context.run("python3 manage.py fill_sample_data")
