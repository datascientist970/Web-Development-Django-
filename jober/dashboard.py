from grappelli.dashboard import modules, Dashboard

class CustomIndexDashboard(Dashboard):
    """
    Custom Dashboard for Job Portal Admin Panel.
    """

    def init_with_context(self, context):
        # Section 1: Job Management
        self.children.append(
            modules.Group(
                title="Job Management",
                column=1,
                collapsible=True,
                children=[
                    modules.ModelList(
                        title="Jobs",
                        models=("jobs.models.Job",),
                    ),
                    modules.ModelList(
                        title="Job Applications",
                        models=("jobs.models.Application",),
                    ),
                    modules.ModelList(
                        title="Job Categories",
                        models=("jobs.models.Category",),
                    ),
                ],
            )
        )

        # Section 2: User Management (Employers & Job Seekers)
        self.children.append(
            modules.Group(
                title="User Management",
                column=1,
                collapsible=True,
                children=[
                    modules.ModelList(
                        title="Employers",
                        models=("users.models.Employer",),
                    ),
                    modules.ModelList(
                        title="Job Seekers",
                        models=("users.models.JobSeeker",),
                    ),
                ],
            )
        )

        # Section 3: Site & Settings
        self.children.append(
            modules.Group(
                title="Site Settings",
                column=2,
                collapsible=True,
                children=[
                    modules.ModelList(
                        title="General Settings",
                        models=("django.contrib.sites.models.Site",),
                    ),
                    modules.ModelList(
                        title="User Roles & Permissions",
                        models=("django.contrib.auth.*",),
                    ),
                ],
            )
        )

        # Section 4: Recent Activity
        self.children.append(
            modules.RecentActions(
                title="Recent Admin Actions",
                limit=10,
                column=2,
            )
        )
