import random
import time
import uuid
from datetime import datetime
from threading import Thread

from app.api.comment.models import Comment
from app.api.files.models import UserFiles
from app.api.follow.models import Follow
from app.api.interest.models import Interest
from app.api.investment.models import Investment  # was asset and is now investment
from app.api.like.models import Like
from app.api.portfolio.models import Portfolio
from app.api.post.models import Post
from app.api.profile.models import Profile
from app.api.question.models import Question
from app.api.reaction.models import React
from app.api.review.models import Review
from app.api.strategy.models import Strategy
from app.api.update.models import Update
from app.type_tables.asset_type.models import (
    AssetType,
)  # was investment and now is asset_type
from faker import Faker
from fastapi_sqlalchemy import db

from app.api.user.models import User
from app.shared.bases.base_model import ModelMixin

fake = Faker(["en-US"])


def seed_asset_types():
    with db():
        asset_type_names = {
            "Cryptocurrency": "cryptocurrency",
            "Stocks": "stocks",
            "NFTs": "nfts",
            "Real Estate": "real-estate",
            "Startups": "startups",
            "Shoes": "shoes",
            "Watches": "watches",
            "Sports Cards": "sports-cards",
            "Pokémon Cards": "pokemon-cards",
            "Cars": "cars",
            "Commodities": "commodities",
            "Private Companies": "private-companies",
            "Fine Art": "fine-art",
            "Jewelry": "jewelry",
            "Coins": "coins",
        }
        asset_types = asset_type_names.items()
        for title, id in asset_types:
            AssetType.create_asset_type_seeder(title, id)
        print(f"created {len(asset_types)} asset_types")
        db.session.close()


class BaseUsername:
    def __init__(self, base_username: str):
        self.base_username = base_username

    @classmethod
    def random_number(cls, length=8):
        return "".join([str(random.randint(0, 9)) for _ in range(length)])

    @classmethod
    def random_float(cls, digits: int, decimals: int):
        return float(f"{cls.random_number(digits)}.{cls.random_number(decimals)}")

    def base_user_seeder(self, username: str = None):
        if not username:
            username = self.base_username
        with db():
            try:
                self._extracted_from_base_user_seeder_1(username)
            except Exception:
                db.session.close()
                return
            db.session.close()

            print(f"created user: {username}")

    # TODO Rename this here and in `base_user_seeder`
    def _extracted_from_base_user_seeder_1(self, username):
        if user := cls.where(username=username).first():
            User.remove_user(user_id=user.id)
        profile = fake.profile()
        phone = fake.phone_number()
        email_data = fake.email().split("@")
        email = (
            f"{email_data[0]}-{BaseUsername.random_number(10)}@{email_data[1]}"
        )
        user_id = uuid.uuid4()
        User.create_user_seeder(
            id=user_id,
            email=email,
            username=username,
            phone=phone,
            name=fake.name(),
            birthdate=profile.get("birthdate"),
        )


class CreateData():
    def __init__(self, username):
        with db():
            self.username = username
            user = self.where(username=self.username).first()
            self.user_id = user.id
            db.session.close()

    def create_interests(self):
        interests = random.randint(0, 9)
        for _ in range(interests):
            boolean = fake.pybool()
            if boolean:
                asset_types = AssetType.get_all_asset_types()
                asset_type = random.choice(asset_types)
                Interest.create_interest_seeder(
                    owner_id=self.user_id, asset_type_id=asset_type.id
                )

    def create_files(self):
        filename = fake.file_name(category="image")
        file_type = fake.mime_type(category="image")
        UserFiles.create_file_seeder(
            owner_id=self.user_id, s3_object=filename, file_type=file_type
        )

        filename = fake.file_name(category="video")
        file_type = fake.mime_type(category="video")
        UserFiles.create_file_seeder(
            owner_id=self.user_id, s3_object=filename, file_type=file_type
        )

        print(f"created 1 image and 1 video file")

    def create_profile(self):
        files = UserFiles.get_files_by_user_id_seeder(user_id=self.user_id)
        picture = files[0]
        ModelMixin.get_or_create_profile(
            Profile,
            owner_id=self.user_id,
            owner_avatar_id=picture.id,
            bio=fake.paragraph(nb_sentences=5),
        )

        print(f"created profile")

    def create_portfolios(self):
        portfolios = random.randint(1, 9)
        for _ in range(portfolios):
            portfolio = Portfolio.create_portfolio_seeder(
                title=fake.text(max_nb_chars=20), owner_id=self.user_id
            )
            investments = random.randint(1, 9)
            for _ in range(investments):
                price = BaseUsername.random_float(2, 2)
                investment = {
                    "owner_id": self.user_id,
                    "portfolio_id": portfolio.id,
                    "symbol": fake.cryptocurrency_code(),
                    "entry_evaluation": round(
                        price - (price * BaseUsername.random_float(2, 2) / 100), 3
                    ),
                    "price_target": price,
                    "hold_time_unit": f"{BaseUsername.random_number(1)} {random.choice(['weeks', 'days', 'months', 'years'])}",
                    "notes": fake.sentence(nb_words=25),
                }
                Investment.create_investment_seeder(**investment)

            print(f"created {investments} investments")

        print(f"created {portfolios} portfolios")

    def create_strategies(self):
        strategies = random.randint(1, 9)
        for _ in range(strategies):

            boolean = fake.pybool()
            price = 0

            if not boolean:
                price = fake.random_int()

            strategy_data = {
                "owner_id": self.user_id,
                "name": fake.text(max_nb_chars=20),
                "price": price,
                "free": boolean,
                "description_text": fake.sentence(nb_words=25),
                "id": uuid.uuid4(),
            }
            strategy = Strategy.create_strategy_seeder(**strategy_data)

            questions = random.randint(1, 9)
            for _ in range(questions):
                question = {
                    "owner_id": self.user_id,
                    "title": fake.text(max_nb_chars=20),
                    "content": fake.sentence(nb_words=25),
                    "strategy_id": strategy.id,
                }
                Question.create_question_seeder(**question)

            print(f"created {questions} questions")

        print(f"created {strategies} strategies")

    def create_updates(self):
        for portfolio in Portfolio.get_user_portfolios_seeder(self.user_id):
            portfolio_updates = random.randint(1, 9)
            for _ in range(portfolio_updates):
                portfolio_data = {
                    "owner_id": self.user_id,
                    "title": fake.text(max_nb_chars=20),
                    "content": fake.sentence(nb_words=25),
                    "portfolio_id": portfolio.id,
                }
                Update.create_update_seeder(**portfolio_data)

            print(f"created {portfolio_updates} portfolio_updates")

        for strategy in Strategy.get_user_strategies_seeder(self.user_id):

            strategy_updates = random.randint(1, 9)
            for _ in range(strategy_updates):
                strategy_data = {
                    "owner_id": self.user_id,
                    "title": fake.text(max_nb_chars=20),
                    "content": fake.sentence(nb_words=25),
                    "strategy_id": strategy.id,
                }
                Update.create_update_seeder(**strategy_data)

            print(f"created {strategy_updates} strategy_updates")

    def create_posts(self):
        posts = random.randint(1, 30)
        for _ in range(posts):
            post_data = {
                "owner_id": self.user_id,
                "content": fake.sentence(nb_words=25),
                "draft": False,
                "timestamp": fake.date_this_month(),
            }
            Post.create_post_seeder(**post_data)

        print(f"created {posts} posts")


# noinspection DuplicatedCode
class IterationData:
    def __init__(
            self,
            user_id,
            target_user_id,
            target_user_username,
            skip_portfolio=False,
            skip_strategy=False,
    ):
        self.user_id = user_id
        self.target_user_id = target_user_id
        self.target_user_username = target_user_username
        self.skip_portfolio = skip_portfolio
        self.skip_strategy = skip_strategy

    def create_follows(self):
        Follow.create_follow_seeder(
            owner_id=self.user_id,
            following_user_id=self.target_user_id,
        )

        print(f"followed {self.target_user_username}")

        follow_count = 0

        if not self.skip_portfolio:
            for portfolio in Portfolio.get_user_portfolios_seeder(
                    user_id=self.target_user_id
            ):
                boolean = fake.pybool()
                if boolean:
                    follow_count += 1
                    follow_data = {
                        "owner_id": self.user_id,
                        "following_portfolio_id": portfolio.id,
                        "timestamp": fake.date_this_month(),
                    }
                    Follow.create_follow_seeder(**follow_data)

        print(f"created {follow_count} portfolio_follows")

        follow_count = 0

        if not self.skip_strategy:
            for strategy in Strategy.get_user_strategies_seeder(
                    user_id=self.target_user_id
            ):
                boolean = fake.pybool()
                if boolean:
                    follow_count += 1
                    follow_data = {
                        "owner_id": self.user_id,
                        "following_strategy_id": strategy.id,
                        "timestamp": fake.date_this_month(),
                    }
                    Follow.create_follow_seeder(**follow_data)

            print(f"created {follow_count} strategy_follows")

    def create_reviews(self):
        review_count = 0

        if not self.skip_portfolio:
            for portfolio in Portfolio.get_user_portfolios_seeder(self.target_user_id):
                boolean = fake.pybool()
                if boolean:
                    review_count += 1
                    review_data = {
                        "owner_id": self.user_id,
                        "portfolio_id": portfolio.id,
                        "content": fake.sentence(nb_words=25),
                        "rating": random.randint(1, 5),
                        "timestamp": fake.date_this_month(),
                    }
                    Review.create_review_seeder(**review_data)

        print(f"created {review_count} portfolio_reviews")

        review_count = 0

        if not self.skip_strategy:
            for strategy in Strategy.get_user_strategies_seeder(self.target_user_id):
                boolean = fake.pybool()
                if boolean:
                    review_count += 1
                    strategy_data = {
                        "owner_id": self.user_id,
                        "strategy_id": strategy.id,
                        "content": fake.sentence(nb_words=25),
                        "rating": random.randint(1, 5),
                        "timestamp": fake.date_this_month(),
                    }
                    Review.create_review_seeder(**strategy_data)

            print(f"created {review_count} strategy_reviews")

    def create_likes(self):
        like_count = 0

        for post in Post.get_user_posts_seeder(self.target_user_id):
            boolean = fake.pybool()
            if boolean:
                like_count += 1
                Like.add_like_seeder(
                    owner_id=self.user_id,
                    liked_post_id=post.id,
                    timestamp=fake.date_this_month(),
                )

        print(f"created {like_count} post_likes")

        like_count = 0

        for post in Post.get_user_posts_seeder(self.target_user_id):
            for comment in Comment.get_post_comments_by_id_seeder(post.id):
                boolean = fake.pybool()
                if boolean:
                    like_count += 1
                    Like.add_like_seeder(
                        owner_id=self.user_id,
                        liked_comment_id=comment.id,
                        timestamp=fake.date_this_month(),
                    )

        print(f"created {like_count} comment_likes")
        like_count = 0

        if not self.skip_strategy:
            for strategy in Strategy.get_user_strategies_seeder(self.target_user_id):
                for review in Review.get_reviews_seeder(strategy_id=strategy.id):
                    boolean = fake.pybool()
                    if boolean:
                        like_count += 1
                        Like.add_like_seeder(
                            owner_id=self.user_id,
                            liked_review_id=review.id,
                            timestamp=fake.date_this_month(),
                        )

            print(f"created {like_count} strategy_review_likes")

        like_count = 0

        if not self.skip_portfolio:
            for portfolio in Portfolio.get_user_portfolios_seeder(self.target_user_id):
                for review in Review.get_reviews_seeder(portfolio_id=portfolio.id):
                    boolean = fake.pybool()
                    if boolean:
                        like_count += 1
                        Like.add_like_seeder(
                            owner_id=self.user_id,
                            liked_review_id=review.id,
                            timestamp=fake.date_this_month(),
                        )

            print(f"created {like_count} portfolio_review_likes")

    def create_comments(self):
        comment_count = 0

        if not self.skip_portfolio:
            for portfolio in Portfolio.get_user_portfolios_seeder(self.target_user_id):
                for update in Update.get_updates_seeder(portfolio_id=portfolio.id):
                    boolean = fake.pybool()
                    if boolean:
                        comment_count += 1
                        comment_data = {
                            "owner_id": self.user_id,
                            "content": fake.sentence(nb_words=25),
                            "commented_update_id": update.id,
                            "timestamp": fake.date_this_month(),
                        }
                        Comment.add_comment_seeder(**comment_data)

            print(f"created {comment_count} portfolio_update_comments")

        comment_count = 0
        if not self.skip_strategy:
            for strategy in Strategy.get_user_strategies_seeder(self.target_user_id):
                for update in Update.get_updates_seeder(strategy_id=strategy.id):
                    boolean = fake.pybool()
                    if boolean:
                        comment_count += 1
                        comment_data = {
                            "owner_id": self.user_id,
                            "content": fake.sentence(nb_words=25),
                            "commented_update_id": update.id,
                            "timestamp": fake.date_this_month(),
                        }
                        Comment.add_comment_seeder(**comment_data)

            print(f"created {comment_count} strategy_update_comments")

        comment_count = 0

        for post in Post.get_user_posts_seeder(self.target_user_id):
            boolean = fake.pybool()
            if boolean:
                comment_count += 1
                comment_data = {
                    "owner_id": self.user_id,
                    "content": fake.sentence(nb_words=25),
                    "commented_post_id": post.id,
                    "timestamp": fake.date_this_month(),
                }
                Comment.add_comment_seeder(**comment_data)

        print(f"created {comment_count} post_comments")

    def create_reactions(self):
        emojis = [
            "\U0001F300",
            "\U0001F320" "\U0001F330",
            "\U0001F335",
            "\U0001F337",
            "\U0001F37C",
            "\U0001F380",
            "\U0001F393",
        ]

        reaction_count = 0

        if not self.skip_portfolio:
            for portfolio in Portfolio.get_user_portfolios_seeder(self.target_user_id):
                for update in Update.get_updates_seeder(portfolio_id=portfolio.id):
                    boolean = fake.pybool()
                    if boolean:
                        reaction_count += 1
                        reaction_data = {
                            "owner_id": self.user_id,
                            "reacted_update_id": update.id,
                            "reaction": random.choice(emojis),
                            "timestamp": fake.date_this_month(),
                        }
                        React.add_react_seeder(**reaction_data)

        print(f"created {reaction_count} portfolio_reactions")

        reaction_count = 0

        if not self.skip_strategy:
            for strategy in Strategy.get_user_strategies_seeder(self.target_user_id):
                for update in Update.get_updates_seeder(strategy_id=strategy.id):
                    boolean = fake.pybool()
                    if boolean:
                        reaction_count += 1
                        reaction_data = {
                            "owner_id": self.user_id,
                            "reacted_update_id": update.id,
                            "reaction": random.choice(emojis),
                            "timestamp": fake.date_this_month(),
                        }
                        React.add_react_seeder(**reaction_data)

            print(f"created {reaction_count} strategy_reactions")


# noinspection DuplicatedCode
class UserGenerator:
    def __init__(
            self,
            base_username: str,
            number_of_users=3000,
            print_stats=False,
            seed_random_user=True,
    ):
        self.base_username = base_username
        self.number_of_users = number_of_users or 1000
        self.print_stats = print_stats
        self.seed_random_user = seed_random_user

    def generate_users_use_threaded(self):

        print("Generating users...")

        threads = [
            Thread(target=self.entry_point, args=(iteration,))
            for iteration in range(int(self.number_of_users))
        ]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        if self.print_stats:
            self.get_user_stats()

    def generate_users_use_loop(self):

        print("Generating users...")

        for iteration in range(self.number_of_users):
            self.entry_point(iteration)

        if self.print_stats:
            self.get_user_stats()

    def entry_point(self, iteration):
        with db():
            number = BaseUsername.random_number
            time.sleep(float(f"0.{number(1)}"))
            profile = fake.profile()
            username = f"{self.base_username}-{iteration}-{number(10)}"

            user = cls.where(username=username).first()

            if user:
                return

            if self.seed_random_user:

                all_users = (
                    db.session.query(User)
                        .filter(User.username.like(f"%{self.base_username}%"))
                        .all()
                )
                target_user = random.choice(all_users)
                if target_user.username == username:
                    target_user = (
                        db.session.query(User)
                            .filter_by(username=self.base_username)
                            .first()
                    )
                try:
                    phone = fake.phone_number()
                    email_data = fake.email().split("@")
                    email = f"{email_data[0]}-{BaseUsername.random_number(10)}@{email_data[1]}"
                    user = User.create_user_seeder(
                        username=username,
                        phone=phone,
                        email=email,
                        name=fake.name(),
                        birthdate=profile.get("birthdate"),
                    )
                except Exception as e:
                    print(e)
                    db.session.close()
                    return

            target_user_username = target_user.username
            target_user_id = target_user.id
            db.session.close()
            with db():
                user_id = user.id
                create_user_data = CreateData(username)
                create_user_data.create_interests()
                create_user_data.create_files()
                create_user_data.create_profile()
                create_user_data.create_portfolios()
                create_user_data.create_strategies()
                create_user_data.create_updates()
                create_user_data.create_posts()
            db.session.close()

            with db():
                n_users = IterationData(user_id, target_user_id, target_user_username)
                n_users.create_follows()
                n_users.create_reviews()
                n_users.create_likes()
                n_users.create_comments()
                n_users.create_reactions()
            db.session.close()

    def get_user_stats(self):
        users = (
            db.session.query(User)
                .filter(User.username.like(f"%{self.base_username}%"))
                .all()
        )
        (
            strategies,
            portfolios,
            comments,
            reactions,
            updates,
            posts,
            questions,
            investments,
            reviews,
            followers,
            post_likes,
            review_likes,
            strategy_follows,
            portfolio_follows,
        ) = [0 for _ in range(14)]
        start = datetime.now()
        for user in users:

            strategies += len(user.strategies)

            for strategy in user.strategies:
                strategy_follows += len(strategy.followers)
                questions += len(strategy.questions)

                updates += len(strategy.updates)
                for update in strategy.updates:
                    comments += len(update.comments)
                    reactions += len(update.reactions)

                reviews += len(strategy.reviews)
                for review in strategy.reviews:
                    review_likes += len(review.likes)

            portfolios += len(user.portfolios)

            for portfolio in user.portfolios:
                portfolio_follows += len(portfolio.followers)
                investments += len(portfolio.investments)

                updates += len(portfolio.updates)
                for update in portfolio.updates:
                    comments += len(update.comments)
                    reactions += len(update.reactions)

                reviews += len(portfolio.reviews)
                for review in portfolio.reviews:
                    review_likes += len(review.likes)

            posts += len(user.posts)
            for post in user.posts:
                post_likes += len(post.likes)

            followers += len(user.followers)

        print(
            f"""

            Creation Stats:
                users: {len(users)}
                strategies: {strategies}
                portfolios: {portfolios}
                investments {investments}
                questions: {questions}
                posts: {posts}
                followers: {followers}
                strategy followers: {strategy_follows}
                portfolio followers: {portfolio_follows}
                reviews: {reviews}
                updates: {updates}
                post likes: {post_likes}
                review likes: {review_likes}
                comments: {comments}
                reactions: {reactions}

            """
        )
        end = datetime.now()
        print(abs(start - end))

    def generate_likes_and_comments_use_thread(self):
        with db():

            users = (
                db.session.query(User).filter(User.username.like(f"%test-user%")).all()
            )

            def iterate():
                user_id = random.choice(users).id
                for _ in range(random.randint(1, 10)):
                    target_user = random.choice(users)
                    if user_id == target_user:
                        pass
                    target_user_id = target_user.id
                    target_user_username = target_user.username
                    data_generator = IterationData(
                        user_id,
                        target_user_id,
                        target_user_username,
                        skip_portfolio=True,
                        skip_strategy=True,
                    )
                    data_generator.create_comments()
                    data_generator.create_likes()

            threads = [Thread(target=iterate) for _ in range(int(self.number_of_users))]
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]
            db.session.close()

    @classmethod
    def generate_likes_and_comments_use_loop(
            cls,
    ):
        with db():
            users = (
                db.session.query(User).filter(User.username.like(f"%test-user%")).all()
            )

        def iterate():
            user_id = random.choice(users).id
            for _ in range(random.randint(1, 10)):
                target_user = random.choice(users)
                if user_id == target_user:
                    pass
                data_generator = IterationData(
                    user_id, target_user, skip_portfolio=True, skip_strategy=True
                )
                data_generator.create_comments()
                data_generator.create_likes()

        for _ in range(50):
            return iterate()
        db.session.close()


def remove_seeded_users(username):
    with db():
        users = db.session.query(User).filter(User.username.like(f"%{username}%")).all()
        count = len(users)
        db.session.query(User).filter(User.username.like(f"%{username}%")).delete(
            synchronize_session=False
        )
        db.session.commit()
        db.session.close()
    print(f"removed {count} users")


def update_seeded_users(
        base_username: str,
        target_model,
        update_field: str = None,
        update_value=None,
        runner_func=None,
        mass_update: bool = False,
):
    with db():

        if mass_update:
            if runner_func:
                update_value = runner_func()
                update_data = {update_field: update_value}
            if not runner_func:
                update_data = {update_field: update_value}
            db.session.query(target_model).filter(
                target_model.owner_id.like(f"%{base_username}%")
            ).update(update_data)
            db.session.commit()
            return True

        data = (
            db.session.query(target_model)
                .filter(target_model.owner_id.like(f"%{base_username}%"))
                .all()
        )
        db.session.close()

        def runner(model, runner_func):
            with db():
                update_value = runner_func()
                update_data = {update_field: update_value}
                print(
                    f"updating {model.id} in {model.__class__.__name__} with data {update_data}"
                )
                db.session.query(target_model).filter_by(id=model.id).update(
                    update_data
                )
                db.session.commit()

        threads = [
            Thread(
                target=runner,
                args=(
                    model,
                    runner_func,
                ),
            )
            for model in data
        ]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        db.session.close()


def update_comments():
    with db():
        data = (
            db.session.query(Comment)
                .filter(Comment.owner_id.like("%test-user-test2%"))
                .all()
        )
        posts = db.session.query(Post).all()
        post_ids = [x.id for x in posts]

        def runner(post_ids, comment):
            boolean = fake.pybool()
            if boolean:
                post = random.choice(post_ids)
                db.session.query(Comment).filter_by(id=comment.id).update(
                    {"commented_post_id": post, "commented_update_id": None}
                )
                print(f"updated {comment.id} now a comment on post {post}")
                db.session.commit()

        threads = [Thread(target=runner, args=(post_ids, comment)) for comment in data]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        db.session.close()


class MainMenu:
    def __init__(self, **kwargs):
        self.selection = kwargs.get("selection")
        self.number_of_users = kwargs.get("number_of_users") or 1000
        self.base_username = kwargs.get("username") or "test-user"

    def seed_base(self):
        """creates a base user with a random number username"""
        number = BaseUsername.random_number()
        base_user_name = BaseUsername(f"{self.base_username}-{number}")
        base_user_name.base_user_seeder()

    def build_generator(self, comments=False):
        self.seed_base()
        user_generator = UserGenerator(
            base_username=self.base_username, number_of_users=self.number_of_users
        )
        if comments is False:
            return user_generator.generate_users_use_threaded
        if comments is True:
            return user_generator.generate_likes_and_comments_use_thread

    def menu_functions(self, run=False):
        def gen_users(comments=False):
            func = self.build_generator(comments=comments)
            if run:
                func()

        funcs = {
            "1": seed_asset_types,
            "2": gen_users,
            "3": gen_users,
            "4": remove_seeded_users,
        }
        return funcs

    def run_menu_function(self):
        funcs = self.menu_functions()
        if self.selection == "2":
            funcs = self.menu_functions(run=True)
        if self.selection == "3":
            funcs = self.menu_functions(run=True)
            funcs[self.selection](comments=True)
        if self.selection == "4":
            funcs[self.selection](username=self.base_username)
        else:
            funcs[self.selection]()


def menu():
    main_menu = """
    \n
    
    Welcome to the Data Seeder.
    Please select your desired capability:

    1) Seed Asset Types
    2) Generate Users
        - Requires numeric input
    3) Generate Likes and Comments
    4) Remove seeded users    """

    _users_input_ = 50
    _main_selection_ = input(main_menu)
    _user_name_ = "test-user"
    if str(_main_selection_) not in MainMenu().menu_functions().keys():
        print("Invalid selection, please select a number shown above.")

    if _main_selection_ == "2" or _main_selection_ == "3":
        _users_input_ = input(
            "Type a number of users (< 3000 due to DB concerns, default 1000)\n"
        )
        _user_name_ = input(
            "Enter a base username (hit enter to use default test-user)\n"
        )
        if _users_input_:
            if int(_users_input_) > 3000:
                print("please enter less than 3000")

    if _main_selection_ == "4":
        _user_name_ = input(
            "Enter a username to remove (hit enter to use default test-user)\n"
        )

    menu_runner = MainMenu(
        number_of_users=_users_input_,
        selection=str(_main_selection_),
        username=_user_name_,
    )
    menu_runner.run_menu_function()


if __name__ == "__main__":
    menu()
